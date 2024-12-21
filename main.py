import argparse
import asyncio
import json
from utils import ConfigValidator


def main():
    parser = argparse.ArgumentParser(description="Asynchronous File Sync Tool")
    parser.add_argument("--config", required=True, help="Path to the configuration file (JSON format)")
    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = json.load(file)

        validator = ConfigValidator(config, raise_exception=True)
        validator.validate()


    # asyncio.run(sync_files(config))


if __name__ == "__main__":
    main()
