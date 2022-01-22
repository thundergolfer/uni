"""
TODO
"""
import argparse
import json
import logging
import pathlib
import shutil
import tarfile
import urllib.request

from typing import List, Optional, Sequence

from dataset import Example, RawEnronDataset

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger().setLevel(logging.DEBUG)

enron_raw_dataset_url_root = "http://www.aueb.gr/users/ion/data/enron-spam/raw/"
enron_dataset_files = {
    "ham": ["beck-s", "farmer-d", "kaminski-v", "kitchen-l", "lokay-m", "williams-w3"],
    "spam": ["BG", "GP", "SH"],
}


def _download_and_extract_dataset(destination_root_path: pathlib.Path):
    logging.info("Downloading raw enron dataset.")
    for key, files in enron_dataset_files.items():
        for value in files:
            logging.info(f"Downloading raw enron dataset file {key}/{value}.")
            dataset_file_url = f"{enron_raw_dataset_url_root}{key}/{value}.tar.gz"
            destination_path = destination_root_path / key / f"{value}.tar.gz"
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(dataset_file_url) as response, open(
                destination_path, "wb"
            ) as out_file:
                shutil.copyfileobj(response, out_file)

            logging.info(f"Extracting raw enron dataset file {key}/{value}")
            tar = tarfile.open(destination_path)
            tar.extractall(destination_path.parent)
            tar.close()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args(argv)

    # TODO(Jonathon): Don't hardcode paths.
    destination_root_path = pathlib.Path(
        (
            "/Users/jonathon/Code/thundergolfer/uni/machine_learning/applications/spam/"
            "a_plan_for_spam/datasets/enron/raw/"
        )
    )
    processed_dataset_path = pathlib.Path(
        "/Users/jonathon/Code/thundergolfer/uni/machine_learning/applications/spam/"
        "a_plan_for_spam/datasets/enron/processed_raw_dataset.json"
    )

    if not args.skip_download:
        _download_and_extract_dataset(destination_root_path=destination_root_path)

    # TODO(Jonathon): This only produces ~50,000 examples.
    # Other links to the dataset claim ~500,000 examples, eg.
    # https://www.kaggle.com/wcukierski/enron-email-dataset
    ds: List[Example] = []
    for pth in destination_root_path.glob("**/*"):
        if pth.is_dir() or str(pth).endswith("tar.gz"):
            continue
        # A single file looks like 'datasets/enron/raw/ham/lokay-m/enron_t_s/25'
        # and it contains a single plain text email.
        is_spam = "raw/spam" in str(pth)
        with open(pth, "r", encoding="latin-1") as f:
            ex = Example(
                email=f.read(),
                spam=is_spam,
            )
            ds.append(ex)

    logging.info("Writing processed raw dataset to file.")
    with open(processed_dataset_path, "w") as f:
        json.dump(ds, f, indent=4)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
