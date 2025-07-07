"""geocode using the google api"""

import os
import time
import googlemaps
import pandas as pd

from helpers import ensure_env_var_exists
from methods_google_geocode import process_google_addresses_from_csv


# create session
API_KEY = ensure_env_var_exists("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=API_KEY)

# settings
filename = "west_ward_short"
address_column_name = "merged_address"
csv_file = f"input{os.sep}{filename}.csv"
output_file = f"output{os.sep}{filename}_output.csv"

# Process all addresses
results_df = process_google_addresses_from_csv(
    google_maps_session=gmaps,
    csv_file_path=csv_file,
    address_column=address_column_name,
)

if not results_df.empty:
    print(f"\nProcessed {len(results_df)} addresses")
    print(f"Successful geocodes: {sum(results_df['status'] == 'SUCCESS')}")

    # Display first few results
    print("\nFirst 5 results:")
    print(
        results_df[
            ["original_address", "formatted_address", "latitude", "longitude", "status"]
        ].head()
    )

    # Save results to new CSV
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to '{output_file}'")
