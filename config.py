import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    DROPBOX_TOKEN: str = os.getenv("DROPBOX_ACCESS_TOKEN")

    source_folder: str = ""
    destination_folder: str = ""
    file_filter: list[str] = []
    max_threads: int = 3

    def populate_from_args(self, args: dict):
        self.source_folder = args.get("sourceFolder")
        self.destination_folder = args.get("destinationFolder")
        self.file_filter = args.get("fileFilter")
        self.max_threads = args.get("maxThreads")


base_config = BaseConfig()
