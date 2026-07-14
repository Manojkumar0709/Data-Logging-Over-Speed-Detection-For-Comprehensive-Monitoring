# ============================================================
# FILE: 05_monitor.py  (MAIN ENTRY POINT)
# PURPOSE: Tie everything together — read sensor, log data,
#          and send alerts if threshold is exceeded.
# RUN WITH: python src/05_monitor.py
# ============================================================
# FLOW:
#   1. Read averaged acceleration from ADXL345 sensor
#   2. Compute net acceleration (remove gravity)
#   3. Upload data to ThingSpeak for live monitoring
#   4. If net acceleration > THRESHOLD:
#        a. Get GPS coordinates
#        b. Build Google Maps link
#        c. Send Email + SMS alert
#   5. Wait 15 seconds (ThingSpeak free tier rate limit)
#   6. Repeat forever
# ============================================================

import time
import os
from dotenv import load_dotenv

# Import our own modules (each file handles one responsibility)
from sensor_adxl345    import read_averaged_acceleration, compute_net_acceleration
from gps_reader        import get_gps_coordinates, build_google_maps_link
from thingspeak_logger import upload_to_thingspeak
from alert_sender      import send_email_alert, send_sms_alert

load_dotenv()  # Load threshold and other settings from .env

# ---- Configuration ----
# How high does net acceleration need to go before an alert fires?
# Units: m/s²  |  Start with 10.0 and tune based on your testing
THRESHOLD = float(os.getenv("ACCELERATION_THRESHOLD", 10.0))

# How long to wait between each reading cycle (seconds)
# ThingSpeak free plan allows 1 update every 15 seconds
LOOP_INTERVAL = 15


def main():
    print("=" * 50)
    print(" Data Logging & Over-Acceleration Monitor")
    print(f" Threshold: {THRESHOLD} m/s²")
    print(" Press Ctrl+C to stop.")
    print("=" * 50)

    cycle = 0

    while True:
        cycle += 1
        print(f"\n[Cycle {cycle}]")

        # --- Step 1: Read sensor data ---
        x, y, z = read_averaged_acceleration(samples=5)
        net_accel = compute_net_acceleration(x, y, z)
        print(f"  Axes  -> X: {x:.2f}  Y: {y:.2f}  Z: {z:.2f} m/s²")
        print(f"  Net Acceleration: {net_accel:.2f} m/s²")

        # --- Step 2: Upload to ThingSpeak ---
        # We upload without GPS here for speed; GPS is fetched only on alert
        upload_to_thingspeak(net_acceleration=net_accel)

        # --- Step 3: Check threshold ---
        if net_accel > THRESHOLD:
            print(f"  ⚠️  THRESHOLD EXCEEDED ({net_accel:.2f} > {THRESHOLD}) m/s²")

            # --- Step 4a: Get GPS location ---
            print("  Fetching GPS coordinates...")
            lat, lon = get_gps_coordinates(timeout=15)

            if lat and lon:
                maps_link = build_google_maps_link(lat, lon)
                print(f"  Location: {maps_link}")
            else:
                maps_link = "GPS fix unavailable"
                print("  GPS fix not available — sending alert without location.")

            # --- Step 4b: Send alerts ---
            send_email_alert(net_accel, maps_link)
            send_sms_alert(net_accel, maps_link)

        else:
            print(f"  ✓ Normal  ({net_accel:.2f} m/s² < threshold {THRESHOLD} m/s²)")

        # --- Step 5: Wait before next cycle ---
        print(f"  Waiting {LOOP_INTERVAL}s for next reading...")
        time.sleep(LOOP_INTERVAL)


# Python convention: only run main() when this file is executed directly
if __name__ == "__main__":
    main()
