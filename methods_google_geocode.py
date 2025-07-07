"""geocode using the google api"""
import time
import pandas as pd


def geocode_address_with_google(
    google_maps_session: object, address: str
) -> dict[str, any]:
    """
    Geocode a single address and return structured data.

    Args:
        address (str): The address to geocode

    Returns:
        Dict containing geocoding results or error info
    """
    try:
        geocode_result = google_maps_session.geocode(address)

        if not geocode_result:
            return {
                "original_address": address,
                "status": "NO_RESULTS",
                "formatted_address": None,
                "place_id": None,
                "types": None,
                "latitude": None,
                "longitude": None,
                "location_type": None,
                "subpremise": None,
                "street_number": None,
                "route": None,
                "locality": None,
                "administrative_area_level_2": None,
                "administrative_area_level_1": None,
                "country": None,
                "postal_code": None,
            }

        # Take the first result (most relevant)
        result = geocode_result[0]

        # Extract address components
        components = {}
        for component in result.get("address_components", []):
            for comp_type in component.get("types", []):
                components[comp_type] = component.get("long_name")

        # Extract geometry info
        geometry = result.get("geometry", {})
        location = geometry.get("location", {})

        return {
            "original_address": address,
            "status": "SUCCESS",
            "formatted_address": result.get("formatted_address"),
            "place_id": result.get("place_id"),
            "types": ", ".join(result.get("types", [])),
            "latitude": location.get("lat"),
            "longitude": location.get("lng"),
            "location_type": geometry.get("location_type"),
            "subpremise": components.get("subpremise"),
            "street_number": components.get("street_number"),
            "route": components.get("route"),
            "locality": components.get("locality"),
            "administrative_area_level_2": components.get(
                "administrative_area_level_2"
            ),
            "administrative_area_level_1": components.get(
                "administrative_area_level_1"
            ),
            "country": components.get("country"),
            "postal_code": components.get("postal_code"),
        }

    except Exception as e:
        return {
            "original_address": address,
            "status": f"ERROR: {str(e)}",
            "formatted_address": None,
            "place_id": None,
            "types": None,
            "latitude": None,
            "longitude": None,
            "location_type": None,
            "subpremise": None,
            "street_number": None,
            "route": None,
            "locality": None,
            "administrative_area_level_2": None,
            "administrative_area_level_1": None,
            "country": None,
            "postal_code": None,
        }


def process_google_addresses_from_csv(
    google_maps_session: object,
    csv_file_path: str,
    address_column: str = "address",
    delay: float = 0.1,
) -> pd.DataFrame:
    """
    Read addresses from CSV and geocode them all.

    Args:
        csv_file_path (str): Path to the CSV file
        address_column (str): Name of the column containing addresses
        delay (float): Delay between API calls to avoid rate limiting

    Returns:
        pd.DataFrame: DataFrame with geocoding results
    """
    # Read the CSV file
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
        return pd.DataFrame()

    # Check if address column exists
    if address_column not in df.columns:
        print(f"Error: Column '{address_column}' not found in CSV.")
        print(f"Available columns: {list(df.columns)}")
        return pd.DataFrame()

    # Get unique addresses to avoid duplicate API calls
    unique_addresses = df[address_column].dropna().unique()

    print(f"Processing {len(unique_addresses)} unique addresses...")

    # Geocode each address
    results = []
    for i, address in enumerate(unique_addresses):
        print(f"Processing {i+1}/{len(unique_addresses)}: {address}")

        result = geocode_address_with_google(google_maps_session, address)
        results.append(result)

        # Add delay to respect rate limits
        if delay > 0:
            time.sleep(delay)

    # Create DataFrame from results
    results_df = pd.DataFrame(results)

    # Merge back with original DataFrame to preserve any additional columns
    # This handles cases where multiple rows have the same address
    merged_df = df.merge(
        results_df, left_on=address_column, right_on="original_address", how="left"
    )

    return merged_df
