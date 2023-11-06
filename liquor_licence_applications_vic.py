"""Class for interacting with the VCGLR website"""

from dotenv import load_dotenv
from custom_selenium import WebPuppet
from helpers import wait_with_message
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


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

        # this makes an instance of our parent class
        super().__init__()

    def scrape(self) -> object:
        """Goes to application page and does the scrape

        Args:
            browser (object): selenium browser object

        Returns:
            object: selenium browser object
        """

        self.browser.get(self.url)
        wait_with_message("waiting to load page", 2)

        # find all forms
        forms = self.browser.find_elements(By.XPATH, "//form[@name='menu_body']")

        # we want the third one - the applications
        forms[2].submit()

        wait_with_message("waiting after changing form", 2)

        #!todo make this a loop for all items
        # save separate files
        # process
        # merge

        # find local gov control
        local_gov_menu = Select(
            self.browser.find_element(By.XPATH, "//select[@name='local_gov_area']")
        )

        # select first local gov
        #!Todo loop through all - load from another method
        local_gov_menu.select_by_visible_text("ALPINE SHIRE COUNCIL")

        wait_with_message("waiting after changing local gov", 3)

        # submit form
        self.browser.find_element(By.XPATH, "//input[@name='Submit']").click()

        wait_with_message("waiting after submit", 5)

        # clean up data

        results = self.browser.find_elements(By.XPATH, "//div[@class='result']")
        # print(results)

        for result in results:
            # print(result)
            items = result.find_elements(By.XPATH, "//div[@class='result-details']")

            for item in items:
                print(item.text)
