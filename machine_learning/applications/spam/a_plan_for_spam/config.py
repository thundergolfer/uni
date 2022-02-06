import os

mail_server_addr = ("localhost", 1024)
mail_receiver_addr = ("localhost", 1025)
spam_detect_api_addr = ("localhost", 8080)
spam_detect_model_tag = (
    "sha256.C6FBAC9A1EA5A3E40DC593F403F6C986E30ECB1DD5538D514A91381F7B4B1EAA"
)

logging_format_str = "%(asctime)s %(levelname)s %(message)s"
logging_file_path_root = os.environ.get("LOGGING_FILE_PATH_ROOT") or "logs/"

spam_models_destination = "models/"
spam_model_tags_db_filepath = f"{spam_models_destination}/model_tags.db"

datasets_path_root = os.environ.get("DATASETS_PATH_ROOT") or "datasets/"
dataset_subpath = os.environ.get("DATASET_SUBPATH") or "enron/clean/dataset.json"
