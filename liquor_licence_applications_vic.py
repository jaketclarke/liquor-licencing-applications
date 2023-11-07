"""Class for interacting with the VCGLR website"""

import os
from dotenv import load_dotenv
from custom_selenium import WebPuppet
from helpers import create_directory_if_not_exists, wait_with_message
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd


class LiquorLicenceApplicationsVic(WebPuppet):
    """Class for interacting with the VCGLR website"""

    def __init__(self) -> "LiquorLicenceApplicationsVic":
        """Create instance of our API class

        Args:
            file_prefix (str): prefix to chuck in front of our
        """

        # we can add magic specific to this we want to do here
        load_dotenv()
        self.url = "https://liquor.vcglr.vic.gov.au/alarm_internet/alarm_internet.ASP?WCI=index_action&WCU"
        self.applications = []
        self.lga_names = []

        # this makes an instance of our parent class
        super().__init__()

    def scrape(self) -> object:
        """Goes to application page and does the scrape

        Args:
            browser (object): selenium browser object

        Returns:
            object: selenium browser object
        """

        # select first local gov
        #!Todo loop through all - load from another method
        lga = "ALPINE SHIRE COUNCIL"
        self.get_data_for_a_local_gov(lga)

        lga = "ARARAT RURAL CITY COUNCIL"
        self.get_data_for_a_local_gov(lga)

    def export_data(self):
        df = pd.DataFrame(self.applications)

        create_directory_if_not_exists(self.output_directory)

        df.to_csv(
            f"{self.output_directory}{os.sep}{self.output_filename}.csv", index=False
        )

    def get_lgas(self):
        self.browser.get(self.url)
        wait_with_message("waiting to load page", 2)

        # find all forms
        forms = self.browser.find_elements(By.XPATH, "//form[@name='menu_body']")

        # we want the third one - the applications
        forms[2].submit()

        wait_with_message("waiting after changing form", 2)

        # find local gov control
        local_gov_menu = Select(
            self.browser.find_element(By.XPATH, "//select[@name='local_gov_area']")
        )

        options = [x.text for x in local_gov_menu.options]

        # remove first element - empty string - from list
        options = options[1:]

        self.lga_names = options

        wait_with_message("waiting after changing local gov", 3)

    def get_data_for_a_local_gov(self, lga):
        self.browser.get(self.url)
        wait_with_message("waiting to load page", 2)

        # find all forms
        forms = self.browser.find_elements(By.XPATH, "//form[@name='menu_body']")

        # we want the third one - the applications
        forms[2].submit()

        wait_with_message("waiting after changing form", 2)
        # find local gov control
        local_gov_menu = Select(
            self.browser.find_element(By.XPATH, "//select[@name='local_gov_area']")
        )

        local_gov_menu.select_by_visible_text(lga)

        wait_with_message("waiting after changing local gov", 3)

        # submit form
        self.browser.find_element(By.XPATH, "//input[@name='Submit']").click()

        wait_with_message("waiting after submit", 5)

        # clean up data

        results = self.browser.find_elements(By.XPATH, "//div[@class='result']")

        for result in results:
            tidy_result = {}
            tidy_result["lga"] = lga
            tidy_result["id"] = results.index(result)

            # a block of text with each key value pair on a new line
            textblock = result.text

            for line in textblock.split("\n"):
                # each row in the form
                # "Licence Category: On-Premises Licence"
                # Except a line with both application id and a short title
                # E.g 46837A09 BOB SUGAR FALLS CREEK, FALLS CREEK 3699
                try:
                    # e.g "Licence Category: On-Premises Licence"
                    vals = line.split(":")
                    tidy_result[vals[0].strip()] = vals[1].strip()
                except:
                    # E.g 46837A09 BOB SUGAR FALLS CREEK, FALLS CREEK 3699
                    tidy_result["Application ID"] = line[0:9].strip()
                    tidy_result["Application Name"] = line[9:].strip()

            self.applications.append(tidy_result)
