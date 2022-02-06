"""
This models module uses code and email spam datasets to define and train models which
are serialized as model artefacts to be loaded by the spam detection
server to drive the effectiveness of the spam detection API.

IMPORTANT: Because models are (de)serialized using `pickle`, it's useful to namespace
the models in their own separate module. Originally I had the models defined in a model_trainer.py
module, but when using that module to train models the pickled models would acquire the __main__
namespace. This caused problems when trying to load the models in the spam_detect_server.py module.
"""

import math
import re
from collections import defaultdict

# TODO(Jonathon): Shouldn't need to import this.
from datasets.enron import dataset

from typing import (
    Callable,
    Dict,
    Iterable,
    Set,
)

Email = str
Prediction = float
Dataset = Iterable[dataset.Example]
SpamClassifier = Callable[[Email], Prediction]


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
    all_words = re.findall("[a-z0-9]+", text)  # extract the words
    return set(all_words)


def train_naive_bayes_classifier(ds: Dataset, k: float = 0.5) -> SpamClassifier:
    dataset_tokens: Set[str] = set()
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
            dataset_tokens.add(token)
            if example.spam:
                token_spam_counts[token] += 1
            else:
                token_ham_counts[token] += 1

    def classify(email: str) -> Prediction:
        email_tokens = tokenize(email)
        log_prob_if_spam = log_prob_if_ham = 0.0

        # Iterate through each word in our vocabulary
        for token in dataset_tokens:
            spam = token_spam_counts[token]
            ham = token_ham_counts[token]

            prob_if_spam = (spam + k) / (spam_messages + 2 * k)
            prob_if_ham = (ham + k) / (ham_messages + 2 * k)
            # If *token* appears in the message,
            # add the log probability of seeing it
            if token in email_tokens:
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
