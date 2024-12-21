import os


class ConfigValidator:
    required_keys = {
        "sourceFolder": str,
        "destinationFolder": str,
    }

    optional_keys = {
        "fileFilter": list,
        "doBackup": bool,
        "maxRetries": int,
    }

    def __init__(self, config_obj: dict, raise_exception: bool = False):
        self.config_obj = config_obj
        self.raise_exception = raise_exception

    def validate(self) -> bool | Exception:
        """
        Validate configuration object.
        :return: True if configuration object is valid; otherwise - False.
        """
        ret: bool = False

        try:
            self._validate_required()
            self._validate_optional()
            self._validate_common()

            ret = True
        except (ValueError, TypeError) as e:
            if self.raise_exception:
                raise e
            print(f"Validation error: {e}")

        return ret

    def _validate_required(self):
        for key, expected_type in self.required_keys.items():
            if key not in self.config_obj:
                raise ValueError(f"Missing required key: '{key}'")
            if not isinstance(self.config_obj[key], expected_type):
                raise TypeError(f"Invalid type for key '{key}': "
                                f"Expected {expected_type.__name__}, got {type(self.config_obj[key]).__name__}")

    def _validate_optional(self):
        for key, expected_type in self.optional_keys.items():
            if key in self.config_obj and not isinstance(self.config_obj[key], expected_type):
                raise TypeError(f"Invalid type for key '{key}': "
                                f"Expected {expected_type.__name__}, got {type(self.config_obj[key]).__name__}")

    def _validate_common(self):
        if not os.path.exists(self.config_obj["sourceFolder"]):
            raise ValueError(f"Source directory '{self.config_obj['sourceFolder']}' does not exist.")
        if not os.path.isdir(self.config_obj["sourceFolder"]):
            raise ValueError(f"Source path '{self.config_obj['sourceFolder']}' is not a directory.")
