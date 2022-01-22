import os

mail_server_addr = ("localhost", 1024)
mail_receiver_addr = ("localhost", 1025)
spam_detect_api_addr = ("localhost", 8080)
spam_detect_model_tag = (
    "sha256.3608C2EFD14B78B5CB41BF15B5BE7BB19D0DCE297AEC8AFBE6F0D08B5A8E2F2E"
)

logging_format_str = "%(asctime)s %(levelname)s %(message)s"
logging_file_path_root = os.environ.get("LOGGING_FILE_PATH_ROOT") or "logs/"

spam_models_destination = "models/"
spam_model_tags_db_filepath = f"{spam_models_destination}/model_tags.db"

datasets_path_root = os.environ.get("DATASETS_PATH_ROOT") or "datasets/"
dataset_subpath = os.environ.get("DATASET_SUBPATH") or "enron/clean/dataset.json"
