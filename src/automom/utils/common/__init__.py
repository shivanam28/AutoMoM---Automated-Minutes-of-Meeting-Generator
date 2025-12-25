"""
Common Utility for AutoMoM
--------------------------
Reusable helper functions for:
- Reading YAML config files
- Creating directories
- Saving text data
"""

import os
import yaml
from automom.utils.logger import logger
from automom.utils.exception import AutoMoMException
import sys


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML configuration file and returns its contents as a dictionary.
    """
    try:
        logger.info(f"📖 Loading YAML config: {file_path}")
        with open(file_path, "r", encoding="utf-8") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise AutoMoMException(e, sys) from e


def create_directories(path_list: list):
    """
    Creates directories from a list of paths if they don't already exist.
    """
    try:
        for path in path_list:
            os.makedirs(path, exist_ok=True)
            logger.info(f"📁 Directory ready: {path}")
    except Exception as e:
        raise AutoMoMException(e, sys) from e


def save_text_file(content: str, file_path: str):
    """
    Saves text content to a specified file.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.success(f"💾 File saved: {file_path}")
    except Exception as e:
        raise AutoMoMException(e, sys) from e


__all__ = ["read_yaml_file", "create_directories", "save_text_file"]

# Example usage:
# from automom.utils.common import save_text_file
# save_text_file("Meeting notes...", "data/processed/test.txt")
