"""Class for interacting with the VCGLR website"""

from dotenv import load_dotenv
from custom_selenium import WebPuppet
from helpers import wait_with_message


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
        wait_with_message("waiting to load page", 5)
