# ============================================================
# FILE: 03_thingspeak_logger.py
# PURPOSE: Send sensor data to ThingSpeak cloud for live
#          monitoring and visualization via HTTP API
# REQUIRES: ThingSpeak account + Write API Key in .env file
# LIBRARY: requests, python-dotenv
# ============================================================
# HOW THINGSPEAK WORKS:
#   - Create a free account at https://thingspeak.com
#   - Create a Channel with fields:
#       Field 1: Net Acceleration (m/s²)
#       Field 2: Latitude
#       Field 3: Longitude
#   - Copy your Write API Key and paste it in the .env file
# ============================================================

import requests    # For making HTTP requests to ThingSpeak
import os
from dotenv import load_dotenv   # Reads credentials from .env file

# Load environment variables from .env file
load_dotenv()

# ThingSpeak API endpoint and credentials
THINGSPEAK_URL     = "https://api.thingspeak.com/update"
THINGSPEAK_API_KEY = os.getenv("THINGSPEAK_WRITE_API_KEY")  # From .env


def upload_to_thingspeak(net_acceleration, latitude=None, longitude=None):
    """
    Send a data point to ThingSpeak.
    - field1: net acceleration value
    - field2: GPS latitude  (optional, send None if no GPS fix)
    - field3: GPS longitude (optional)

    Returns True if upload was successful, False otherwise.
    """
    # Build the data payload as a dictionary
    payload = {
        "api_key": THINGSPEAK_API_KEY,
        "field1" : round(net_acceleration, 4),  # Net accel in m/s²
    }

    # Add GPS data only if a valid fix is available
    if latitude is not None:
        payload["field2"] = latitude
    if longitude is not None:
        payload["field3"] = longitude

    try:
        # Send HTTP GET request to ThingSpeak
        response = requests.get(THINGSPEAK_URL, params=payload, timeout=10)

        # ThingSpeak returns the entry ID (a positive integer) on success
        # It returns '0' if the upload failed or rate limit was hit
        if response.text.strip() != "0":
            print(f"ThingSpeak upload OK | Entry ID: {response.text.strip()}")
            return True
        else:
            print("ThingSpeak upload FAILED (returned 0). Check API key or rate limit.")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Network error during ThingSpeak upload: {e}")
        return False


# ---- STANDALONE TEST ----
if __name__ == "__main__":
    print("ThingSpeak Logger Test")
    # Send a dummy value to verify connection
    success = upload_to_thingspeak(
        net_acceleration=3.75,
        latitude=12.9716,
        longitude=77.5946
    )
    print("Upload successful!" if success else "Upload failed. Check credentials.")
