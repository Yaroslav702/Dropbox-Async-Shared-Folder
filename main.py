import argparse
import logging
import json

from services.validators import ArgsValidator
from services.watcher import FolderWatcher

from config import base_config


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("FolderWatcher")

    parser = argparse.ArgumentParser(description="Asynchronous File Sync Tool")
    parser.add_argument("--config", required=True, help="Path to the configuration file (JSON format)")
    args = parser.parse_args()

    with open(args.config, "r") as file:
        args_config = json.load(file)

        validator = ArgsValidator(args_config, raise_exception=True)
        validator.validate()

        base_config.populate_from_args(args_config)

    watcher = FolderWatcher(base_config.source_folder,
                            destination_folder_path=base_config.destination_folder,
                            dropbox_token=base_config.DROPBOX_TOKEN,
                            threads_num=base_config.MAX_THREADS,
                            logger=logger,
                            allowed_extensions=base_config.file_filter)
    watcher.run()


if __name__ == "__main__":
    main()
