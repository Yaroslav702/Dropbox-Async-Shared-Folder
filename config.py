import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    MAX_THREADS: int = 5
    DROPBOX_TOKEN: str = os.getenv("DROPBOX_ACCESS_TOKEN")

    source_folder: str = ""
    destination_folder: str = ""
    file_filter: list[str] = []
    max_retries: int = 0

    def populate_from_args(self, args: dict):
        self.source_folder = args.get("sourceFolder")
        self.destination_folder = args.get("destinationFolder")
        self.file_filter = args.get("fileFilter")
        self.max_retries = args.get("maxRetries")


base_config = BaseConfig()
