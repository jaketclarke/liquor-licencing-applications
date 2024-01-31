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

geocode_output_filepath = f"{OUTPUT_DIRECTORY}{os.sep}{OUTPUT_FILENAME}-geocoded.csv"
input_filepath = f"{OUTPUT_DIRECTORY}{os.sep}{OUTPUT_FILENAME}.csv"
errors_filepath = f"{OUTPUT_DIRECTORY}{os.sep}geocode-errors.json"

# load input
input_filepath = pd.read_csv(input_filepath)
results = []

# create geocode object
amg = AzureMapsGeocode()

# place for errors
errors = []

i = 0
# iterate over data
for index, row in input_filepath.iterrows():
    # every 100th run, sleep - to not spam API
    if index % 100 == 0:
        time.sleep(10)

    # geocode address
    if i < 250:
        try:
            result = amg.geocode_address(row["id"], row["Premises Address"])
            results.append(result)
        except:
            errors.append(result)
            print(result)

        i += 1

with open(errors_filepath, "w") as final:
    json.dump(errors, final)


results_df = pd.DataFrame(results)

#! todo
# remove rows where coordinates are null
# "coordinates": [
#     NaN,
#     NaN
# ]

#! todo
# remove results where state != vic
results_df = results_df.loc[results_df["state"] == "Victoria"]

output = pd.merge(
    left=input_filepath,
    right=results_df,
    left_on="Premises Address",
    right_on="input_address",
    how="left",
)

# remove spaces from header names
output.rename(columns=lambda x: str.lower(x.replace(" ", "_")), inplace=True)

# replace "NaN" in output with something
# comes out unquoted and breaks leaflet
output = output.fillna("-")

output.to_csv(geocode_output_filepath)

#!todo
## drop where lat invalid
output =  output[output['lat'] != '-']

geo_json = to_geojson(
    df=output,
    lat="lat",
    lon="lon",
    properties=[
        "application_id",
        "application_name",
        "application_received_date",
        "premises_address",
        "application_type",
        "public_notice_display_period",
        "applicant",
        "licence_category",
        "licence_number",
        "star_rating",
        "demerit_points",
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
