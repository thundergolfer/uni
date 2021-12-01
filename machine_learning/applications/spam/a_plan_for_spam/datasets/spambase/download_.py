"""
TODO
"""
import logging
import shutil
import urllib.request
import zipfile

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger().setLevel(logging.DEBUG)


def main():
    dataset_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.zip"
    # TODO(Jonathon): Don't hardcode path.
    destination_zip_path = (
        "/Users/jonathon/Code/thundergolfer/uni/machine_learning/applications/spam/"
        "a_plan_for_spam/datasets/spambase/spambase.zip"
    )

    logging.info("Downloading spambase dataset as zipfile.")
    with urllib.request.urlopen(dataset_url) as response, open(
        destination_zip_path, "wb"
    ) as out_file:
        shutil.copyfileobj(response, out_file)

    logging.info("Extracting spambase dataset from zipfile.")
    with zipfile.ZipFile(destination_zip_path) as zf:
        zf.extractall()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
