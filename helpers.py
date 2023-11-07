"""helper functions"""
import os
import time
import shutil
from azure.storage.blob import BlobServiceClient


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


def upload_file_to_blob(
    connection_string: str, container_name: str, blob_path: str, upload_filepath: str
) -> None:
    """Upload a blob to a container from a local filepath

    Args:
        connection_string (str): blob connnection string
        container_name (str): blob container name
        blob_path (str): path to file in blob e.g folder1/test.txt
        upload_filepath (str): where to find it locally e.g. output/test22.txt
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
    except RuntimeError as ex:
        raise RuntimeError("Could not make blob service client") from ex

    try:
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_path
        )
        with open(upload_filepath, mode="rb") as data:
            blob_client.upload_blob(data, overwrite=True)
    except RuntimeError as ex:
        raise RuntimeError(
            f"Could not upload file {upload_filepath} to blob {blob_path}"
        ) from ex
