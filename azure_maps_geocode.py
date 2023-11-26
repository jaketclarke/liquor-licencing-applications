import datetime
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient


class AzureMapsGeocode(object):
    """Class for geocoding with Azure Maps"""

    def __init__(self) -> "AzureMapsGeocode":
        """Class to interact with Azure Maps geocoding service

        Returns:
            AzureMapsGeocode: object to interact with Azure Maps geocoding service
        """
        # import env file
        load_dotenv()

        # put properties in for linting reasons
        self.output_directory = None

        self.run_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

        # set env vars
        env_vars = [
            "OUTPUT_DIRECTORY",
            "OUTPUT_FILENAME",
            "WHERE_AM_I",
            "BLOB_CONTAINER_NAME",
            "BLOB_CONNECTION_STRING",
            "AZURE_SUBSCRIPTION_KEY",
        ]
        # set properties from env vars
        for env_var in env_vars:
            self._set_attr_from_env_var(env_var)

        # set download dir
        # chrome can't handle relative paths so we give it a full path to the output dir below
        self.output_directory = self.output_directory
        self.output_directory_full_path = f"{Path.cwd()}{os.sep}{self.output_directory}"
        logging.info("download directory set to %s", self.output_directory_full_path)

        # default for WHERE_AM_I
        self.where_am_i = os.getenv("WHERE_AM_I", "dev")
        logging.info("set where_am_i to %s", self.where_am_i)

        # load search client
        self.search_client = self._get_search_client()

    def _set_attr_from_env_var(self, env_var: str) -> None:
        try:
            if os.getenv(env_var):
                setattr(self, str.lower(env_var), os.getenv(env_var))
            else:
                raise ValueError(
                    f"The {env_var} field is required - check .env file or github secrets"
                )
        except ValueError as e:
            raise ValueError(
                f"The {env_var} field is required - check .env file or github secrets, {e}"
            ) from e

    def _get_search_client(self) -> None:
        credential = AzureKeyCredential(self.azure_subscription_key)

        search_client = MapsSearchClient(
            credential=credential,
        )

        return search_client
