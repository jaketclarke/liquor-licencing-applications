"""Code to geocode the address field from the liquor licence applications"""
import time
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

# read output
location = f"{OUTPUT_DIRECTORY}{os.sep}{OUTPUT_FILENAME}.csv"

input = pd.read_csv(location)
results = []
for index, row in input.iterrows():
    if index % 10 == 0:
        time.sleep(10)
    
    search_result = search_client.search_address(
        row["Premises Address"]
    )

    res = {}

    res["id"] = search_result.results[0].id
    res["state"] = search_result.results[0].address.country_subdivision
    res["suburb"] = search_result.results[0].address.municipality_subdivision
    res["postcode"] = search_result.results[0].address.postal_code
    res["lat"] = search_result.results[0].position.lat
    res["lon"] = search_result.results[0].position.lon

    results.append(res)

print(results)