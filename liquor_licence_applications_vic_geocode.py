"""Code to geocode the address field from the liquor licence applications"""
import pandas as pd
import os
from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient

from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY")
OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME")
AZURE_SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY")

credential = AzureKeyCredential(AZURE_SUBSCRIPTION_KEY)

search_client = MapsSearchClient(
    credential=credential,
)

search_result = search_client.search_address(
    "1 Treasury Place, East Melbourne VIC 3002"
)
id = search_result.results[0].id
state = search_result.results[0].address.country_subdivision
suburb = search_result.results[0].address.municipality_subdivision
postcode = search_result.results[0].address.postal_code
lat = search_result.results[0].position.lat
lon = search_result.results[0].position.lon
print(id, state, postcode, suburb, lat, lon, id)
