"""helper functions"""
import os
import time
import shutil


def wait_with_message(message: str, wait: float) -> None:
    """wait with a console log

    Args:
        message (str): what to say while we wait
        wait (float): how long to wait (in seconds)
    """
    print(f"{message} | waiting {wait} seconds")
    time.sleep(wait)


def destroy_and_remake_directory(directory: str) -> None:
    """Remove a directory if it exists, then create

    Args:
        directory (str): path to directory
    """

    shutil.rmtree(directory, ignore_errors=True)
    print(f"removed {directory}")

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"created {directory}")


def create_directory_if_not_exists(directory: str) -> None:
    """Create a directory if it does not exist

    Args:
        directory (str): path to directory
    """

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"created {directory}")


def delete_file_if_exists(filepath: str) -> None:
    """Deletes a file if it exists

    Args:
        filepath (str): file/to/delete.text
    """
    if os.path.exists(filepath):
        os.remove(filepath)
