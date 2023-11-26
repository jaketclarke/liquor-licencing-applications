"""Code to geocode the address field from the liquor licence applications"""
import time
import pandas as pd
import os
from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient
from pandas_geojson import to_geojson, write_geojson

from dotenv import load_dotenv

from azure_maps_geocode import AzureMapsGeocode

load_dotenv()

OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY")
OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME")
AZURE_SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY")

amg = AzureMapsGeocode()


# read output
location = f"{OUTPUT_DIRECTORY}{os.sep}{OUTPUT_FILENAME}.csv"

input = pd.read_csv(location)
results = []
for index, row in input.iterrows():
    if index % 10 == 0:
        time.sleep(10)

    result = amg.geocode_address(row['id'], row['Premises Address'])
    results.append(result)
    

results_df = pd.DataFrame(results)

output = pd.merge(left=input, right=results_df, left_on="Premises Address", right_on='input_address', how="left")
output.to_csv(f"{OUTPUT_DIRECTORY}{os.sep}{OUTPUT_FILENAME}-geocoded.csv")

geo_json = to_geojson(
    df=output,
    lat="lat",
    lon="lon",
    properties=[
        "Application ID",
        "Application Name",
        "Application Received Date",
        "Premises Address",
        "Application Type",
        "Public Notice Display Period",
        "Applicant",
        "Licence Category",
        "Licence Number",
        "Star Rating",
        "Demerit Points",
        "state",
        "suburb",
        "postcode",
    ],
)

write_geojson(
    geo_json,
    filename=f"{OUTPUT_DIRECTORY}{os.sep}{OUTPUT_FILENAME}-geocoded.geojson",
    indent=4,
)
