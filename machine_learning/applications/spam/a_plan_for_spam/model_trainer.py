"""
The model trainer uses email spam datasets to train models,
which are serialized as model artefacts to be loaded by the spam detection
server to drive the effectiveness of the spam detection API.
"""
import argparse
import datetime
import hashlib
import json
import logging
import math
import pathlib
import re
import subprocess
from collections import defaultdict

from typing import Any, Callable, Dict, Iterable, NamedTuple, Optional, Union, Sequence, Set

import config
from datasets.enron import dataset

logging.basicConfig(format=config.logging_format_str)
logging.getLogger().setLevel(logging.DEBUG)


Email = str
Prediction = float
SpamClassifier = Callable[[Email], Prediction]
Dataset = Iterable[dataset.Example]
TrainingFunc = Callable[[Dataset], Any]
ModelBuilder = Callable[[Dataset, Optional[TrainingFunc]], SpamClassifier]
# A Classifier is produced by supplying [Dataset AND TrainingFunc] OR [Classifier]
# How to model this? Passing no Dataset and no TrainingFunc to a builder, which just returns
# the Classifier?
# You could do the builder as some kind of functional pipeline. A step in the pipeline can
# modify the Dataset, modify the TrainingFunc, or modify the Classifier. The resulting modifications
# are passed down to the next step. If the Classifier
# isn't present, a step must produce the Classifier.
# That's probably hella overcomplicated though.
#
# def build_classifier(
#     steps: Callable[[Dataset, TrainingFunc, Optional[SpamClassifier]], [Dataset, TrainingFunc, Optional[SpamClassifier]]]
#     final: Callable[[Dataset, TrainingFunc, Optional[SpamClassifier]], SpamClassifier],
# ): ...

MODEL_REGISTRY_FILENAME = "registry.json"


class ClassifierMetadata(NamedTuple):
    impl_name: str
    save_date: str
    git_commit_hash: str


Sha256Hash = str
ModelRegistryMetadata = Dict[Sha256Hash, ClassifierMetadata]


def get_git_revision_hash() -> str:
    return (
        subprocess.check_output(["git", "rev-parse", "--verify", "HEAD"])
        .decode("ascii")
        .strip()
    )


def bad_words_spam_classifier(email: Email) -> Prediction:
    # TODO(Jonathon): Some kind of text cleaner/tokenizer
    tokens = " ".split(email)
    tokens_set = set(tokens)
    bad_words = {
        "sex",
        "xxx",
        "nigerian",
        "teens",
    }
    max_bad_words = 2
    bad_words_count = 0
    for word in bad_words:
        if word in tokens_set:
            bad_words_count += 1
    return 1.0 if bad_words_count > max_bad_words else 0.0


# TODO(Jonathon): Calculate N most popular non-stop-words to use as spam indicators.
# This is basically a smarter version of `bad_words_spam_classifier`, which assumes
# a fixed set of words are always indicators of spam, ignorant of the available dataset.
def build_top_spam_words_classifier(ds: Dataset) -> SpamClassifier:
    def classifier(email: Email) -> Prediction:
        return 0.0
    return classifier


def tokenize(text: str) -> Set[str]:
    text = text.lower()
    all_words = re.findall("[a-z0-9]+", text)  # extract the words, and
    return set(all_words)


def train_naive_bayes_classifier(ds: Dataset, k: float = 0.5) -> SpamClassifier:
    tokens: Set[str] = set()
    token_spam_counts: Dict[str, int] = defaultdict(int)
    token_ham_counts: Dict[str, int] = defaultdict(int)
    spam_messages = ham_messages = 0

    for example in ds:
        if example.spam:
            spam_messages += 1
        else:
            ham_messages += 1

        # Increment word counts
        for token in tokenize(example.email):
            tokens.add(token)
            if example.spam:
                token_spam_counts[token] += 1
            else:
                token_ham_counts[token] += 1

    def classify(email: str) -> Prediction:
        text_tokens = tokenize(email)
        log_prob_if_spam = log_prob_if_ham = 0.0

        # Iterate through each word in our vocabulary
        for token in tokens:
            spam = token_spam_counts[token]
            ham = token_ham_counts[token]

            prob_if_spam = (spam + k) / (spam_messages + 2 * k)
            prob_if_ham = (ham + k) / (ham_messages + 2 * k)
            # If *token* appears in the message,
            # add the log probability of seeing it
            if token in text_tokens:
                log_prob_if_spam += math.log(prob_if_spam)
                log_prob_if_ham += math.log(prob_if_ham)
            # Otherwise add the log probability of _not_ seeing it,
            # which is log(1 - probability of seeing it)
            else:
                log_prob_if_spam += math.log(1.0 - prob_if_spam)
                log_prob_if_ham += math.log(1.0 - prob_if_ham)
        prob_if_spam = math.exp(log_prob_if_spam)
        prob_if_ham = math.exp(log_prob_if_ham)
        return prob_if_spam / (prob_if_spam + prob_if_ham)
    return classify


def serialize_classifier(
    classifier_func: SpamClassifier,
) -> bytes:
    import pickle

    return pickle.dumps(classifier_func)


def store_classifier(
    *,
    classifier_func: SpamClassifier,
    classifier_destination_root: pathlib.Path,
    current_git_commit_hash: str,
) -> pathlib.Path:
    logging.info("Storing spam classifier to model registry.")

    serialized_classifier = serialize_classifier(classifier_func)
    hash_base = hashlib.sha256(serialized_classifier).hexdigest().upper()
    ser_clssfr_hash = f"sha256.{hash_base}"

    logging.info(f"Serialized classifier's hash is {ser_clssfr_hash}")

    model_registry_metadata = load_classifier_registry_metadata(
        classifier_destination_root=classifier_destination_root,
    )

    classifier_dest_path = classifier_destination_root / ser_clssfr_hash
    if classifier_dest_path.is_file():
        logging.warning(
            (
                f"Classifier {ser_clssfr_hash} already exists. No need to save again. "
                "Consider caching model training to save compute cycles."
            )
        )
    else:
        logging.info(f"Saving classifier to file at '{classifier_dest_path}'")
        classifier_dest_path.write_bytes(serialized_classifier)

    logging.info(
        f"Updating models registry metadata to include information about {ser_clssfr_hash}"
    )
    metadata = ClassifierMetadata(
        impl_name=classifier_name_from_function(classifier_func),
        save_date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        git_commit_hash=current_git_commit_hash,
    )
    store_classifier_registry_metadata(
        model_registry_metadata=model_registry_metadata,
        classifier_sha256_hash=ser_clssfr_hash,
        classifier_metadata=metadata,
        classifier_destination_root=classifier_destination_root,
    )
    logging.info("Done! Classifier model stored 📦.")
    return classifier_dest_path


def classifier_name_from_function(classifier_func: SpamClassifier) -> str:
    # NOTE: This may be buggy, and create name clashes or ambiguity.
    return classifier_func.__qualname__


def load_classifier_registry_metadata(
    *,
    classifier_destination_root: pathlib.Path,
):
    model_registry_metadata_filepath = (
        classifier_destination_root / MODEL_REGISTRY_FILENAME
    )
    if not model_registry_metadata_filepath.exists():
        # Create registry metadata file on first save of a model.
        model_registry_metadata_filepath.write_text("{}")

    with open(model_registry_metadata_filepath, "r") as model_registry_f:
        data = json.load(model_registry_f)
    model_registry_metadata: ModelRegistryMetadata = {
        key: ClassifierMetadata(
            impl_name=value["impl_name"],
            save_date=value["save_date"],
            git_commit_hash=value["git_commit_hash"],
        )
        for key, value in data.items()
    }
    return model_registry_metadata


def retrieve_classifier_registry_metadata(
    *,
    model_registry_metadata: ModelRegistryMetadata,
    classifier_sha256_hash: str,
) -> Optional[ClassifierMetadata]:
    return model_registry_metadata.get(classifier_sha256_hash)


def store_classifier_registry_metadata(
    *,
    model_registry_metadata: ModelRegistryMetadata,
    classifier_sha256_hash: str,
    classifier_metadata: ClassifierMetadata,
    classifier_destination_root: pathlib.Path,
) -> None:
    existing_metadata = retrieve_classifier_registry_metadata(
        model_registry_metadata=model_registry_metadata,
        classifier_sha256_hash=classifier_sha256_hash,
    )
    if existing_metadata is not None:
        logging.debug("Classifier with matching hash found in registry.")
        # compare new metadata with old to detect registry corruption or
        # strange renaming.
        if classifier_metadata.impl_name != existing_metadata.impl_name:
            raise RuntimeError(
                "Existing classifier with identical sha256 hash to current classifier found "
                "with conflicting metadata. "
                "Something has gone wrong."
            )
    model_registry_metadata_dict = {
        key: value._asdict() for key, value in model_registry_metadata.items()
    }
    # NOTE: Potentially overwrites with new metadata.
    model_registry_metadata_dict[classifier_sha256_hash] = classifier_metadata._asdict()
    with open(
        classifier_destination_root / MODEL_REGISTRY_FILENAME, "w"
    ) as model_registry_f:
        json.dump(model_registry_metadata_dict, model_registry_f, indent=4)


def load_serialized_classifier(
    *,
    classifier_sha256_hash: str,
    classifier_destination_root: pathlib.Path,
) -> SpamClassifier:
    # TODO: Check registry first???

    def check_integrity(*, expected_hash: str, actual_hash: str) -> None:
        if not expected_hash == actual_hash:
            err_msg = f"Shasum integrity check failure. Expected '{expected_hash}' but got '{actual_hash}'"
            raise ValueError(err_msg)

    expected_prefix = "sha256."
    if not classifier_sha256_hash.startswith(expected_prefix):
        raise ValueError(
            f"Classifier sha256 hashes are expected to start with the prefix '{expected_prefix}"
        )

    classifier_path = classifier_destination_root / classifier_sha256_hash
    with open(classifier_path, "rb") as f:
        classifier_bytes = f.read()

    hash_base = hashlib.sha256(classifier_bytes).hexdigest().upper()
    loaded_classifier_hash = f"sha256.{hash_base}"

    check_integrity(
        expected_hash=classifier_sha256_hash,
        actual_hash=loaded_classifier_hash,
    )
    import pickle

    return pickle.loads(classifier_bytes)


def main(argv: Union[Sequence[str], None] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-registry-root", required=True)
    args = parser.parse_args(argv)
    model_registry_root = pathlib.Path(args.model_registry_root)

    store_classifier(
        classifier_func=bad_words_spam_classifier,
        classifier_destination_root=model_registry_root,
        current_git_commit_hash=get_git_revision_hash(),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
