"""Code to geocode the address field from the liquor licence applications"""
import json
import time
import pandas as pd
import os
from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient
from pandas_geojson import to_geojson, write_geojson

from dotenv import load_dotenv

from azure_maps_geocode import AzureMapsGeocode

# where is the input file?
load_dotenv()

OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY")
OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME")

location = f"{OUTPUT_DIRECTORY}{os.sep}{OUTPUT_FILENAME}.csv"
errors_filepath = f"{OUTPUT_DIRECTORY}{os.sep}geocode-errors.json"

# load input
input = pd.read_csv(location)
results = []

# create geocode object
amg = AzureMapsGeocode()

# place for errors
errors = []

# iterate over data
for index, row in input.iterrows():
    # every 100th run, sleep - to not spam API
    if index % 100 == 0:
        time.sleep(10)

    # geocode address
    try:
        result = amg.geocode_address(row["id"], row["Premises Address"])
        results.append(result)
    except:
        errors.append(result)
        print(result)

with open(errors_filepath, "w") as final:
    json.dump(errors, final)

results_df = pd.DataFrame(results)

output = pd.merge(
    left=input,
    right=results_df,
    left_on="Premises Address",
    right_on="input_address",
    how="left",
)
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
