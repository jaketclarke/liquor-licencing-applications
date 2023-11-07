"""class for interacting with the websites via selenium"""


import datetime
import os
import os.path
import logging
from pathlib import Path
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException

from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


class WebPuppet(object):
    """Class for interacting with websites via selenium"""

    def __init__(self) -> "WebPuppet":
        """_summary_

        Returns:
            WebPuppet: object to interact with websites via selenium
        """
        # import env file
        load_dotenv()

        # put properties in for linting reasons
        self.output_directory = None

        self.run_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

        # set env vars
        env_vars = [
            "OUTPUT_DIRECTORY",
            "OUTPUT_FILENAME"
        ]

        # set properties from env vars
        for env_var in env_vars:
            self._set_attr_from_env_var(env_var)

        # set download dir
        # chrome can't handle relative paths so we give it a full path to the output dir below
        self.output_directory = self.output_directory
        self.output_directory_full_path = f"{Path.cwd()}{os.sep}{self.output_directory}"
        logging.info("download directory set to %s", self.output_directory_full_path)

        # set env
        self.where_am_i = os.getenv("WHERE_AM_I", "dev")
        logging.info("set where_am_i to %s", self.where_am_i)

        # set chrome options
        self._get_chrome_options()

        # empty browser object
        self.browser = None

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

    def _get_chrome_options(self) -> None:
        """Craft selenium chrome options

        Args:
            download_directory (str, optional): path to download to from Chrome. Defaults "output".

        """
        chrome_options = Options()

        # if an env var is set to production, run headless
        load_dotenv()
        if "Production" in os.getenv("WHERE_AM_I", "dev"):
            logging.info("running in production, adding headless mode")
            chrome_options.add_argument("--headless")  # Ensure GUI is off in prod

        options = [
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
        for option in options:
            chrome_options.add_argument(option)

        prefs = {
            "download.default_directory": self.output_directory_full_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        self.chrome_options = chrome_options

    def get_browser(self) -> object:
        """Function to get selenium browser

        Args:
            download_directory (str, optional): output directory for chrome. Defaults to "output"

        Returns:
            webdriver.chrome(): selenium webdriver
        """

        # Choose Chrome Browser
        browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=self.chrome_options,
        )

        self.browser = browser

    def cancel_alert_if_exists(self) -> object:
        """Will take a selenium browser object, and cancel an alert if one is there

        Args:
            browser (object): selenium browser object

        Returns:
            object: selenium browser object
        """
        try:
            WebDriverWait(self.browser, 5).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            alert.dismiss()
            logging.info("alert was present, cancelled")
        except TimeoutException:
            logging.info("no alert")
