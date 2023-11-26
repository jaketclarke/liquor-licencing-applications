""" Run a scrape of the latest liquor licence applications in Vic"""
import logging
import os
import sys

from dotenv import load_dotenv
from helpers import upload_file_to_blob, get_now_in_melbourne_string
from liquor_licence_applications_vic import LiquorLicenceApplicationsVic

load_dotenv()

# configure logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

webpuppet = LiquorLicenceApplicationsVic()
webpuppet.get_browser()
webpuppet.scrape()
webpuppet.export_data()

upload_file_to_blob(
    os.getenv("BLOB_CONNECTION_STRING"),
    os.getenv("BLOB_CONTAINER_NAME"),
    f"applications{os.sep}vic-applications-{get_now_in_melbourne_string()}.csv",
    f"{webpuppet.output_directory}{os.sep}{webpuppet.output_filename}.csv",
)

upload_file_to_blob(
    os.getenv("BLOB_CONNECTION_STRING"),
    os.getenv("BLOB_CONTAINER_NAME"),
    f"applications{os.sep}vic-applications-latest.csv",
    f"{webpuppet.output_directory}{os.sep}{webpuppet.output_filename}.csv",
)
