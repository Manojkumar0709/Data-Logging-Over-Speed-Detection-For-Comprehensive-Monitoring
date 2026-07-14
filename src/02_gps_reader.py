# ============================================================
# FILE: 02_gps_reader.py
# PURPOSE: Read GPS coordinates (latitude, longitude) using
#          the GSM/GPRS/GPS HAT module over UART/Serial
# INTERFACE: UART (Serial port /dev/ttyS0 or /dev/ttyAMA0)
# LIBRARY: pyserial, pynmea2
# ============================================================
# HARDWARE CONNECTIONS (GPS HAT --> Raspberry Pi Zero WH)
#   The HAT plugs directly onto the 40-pin GPIO header.
#   GPS communicates via UART:
#     TX (HAT) --> GPIO15 / RXD (Pin 10)
#     RX (HAT) --> GPIO14 / TXD (Pin 8)
# NOTE: Disable the Pi's serial console first:
#   Run: sudo raspi-config --> Interface Options --> Serial
#   Disable login shell, Enable serial port hardware
# ============================================================

import serial    # pyserial: for reading serial/UART data
import pynmea2   # For parsing NMEA GPS sentences
import time

# --- Serial port configuration ---
SERIAL_PORT = "/dev/ttyS0"   # Change to /dev/ttyAMA0 if needed
BAUD_RATE   = 9600            # Standard GPS baud rate


def get_gps_coordinates(timeout=10):
    """
    Open the serial port and read GPS NMEA sentences.
    Returns (latitude, longitude) as floats when a valid fix is found.
    Returns (None, None) if no fix found within the timeout period.

    NMEA sentence we look for: $GPRMC or $GPGGA
    """
    try:
        # Open the serial connection to the GPS module
        gps_serial = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)

        start_time = time.time()

        while (time.time() - start_time) < timeout:
            raw_line = gps_serial.readline()   # Read one line of NMEA data

            try:
                # Decode bytes to string and strip whitespace
                line = raw_line.decode('ascii', errors='replace').strip()

                # We only care about GPRMC sentences (they contain lat/lon + status)
                if line.startswith('$GPRMC'):
                    msg = pynmea2.parse(line)  # Parse the NMEA sentence

                    # 'status' == 'A' means the GPS has an active fix
                    if msg.status == 'A':
                        latitude  = msg.latitude   # Decimal degrees (e.g. 12.9716)
                        longitude = msg.longitude  # Decimal degrees (e.g. 77.5946)
                        gps_serial.close()
                        return latitude, longitude

            except pynmea2.ParseError:
                # Some lines may be incomplete or corrupted — skip them
                continue

        gps_serial.close()
        print("GPS timeout: No valid fix received.")
        return None, None

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None, None


def build_google_maps_link(latitude, longitude):
    """
    Create a clickable Google Maps URL from lat/lon coordinates.
    Example: https://maps.google.com/?q=12.9716,77.5946
    """
    return f"https://maps.google.com/?q={latitude},{longitude}"


# ---- STANDALONE TEST ----
if __name__ == "__main__":
    print("GPS Reader Test --- Waiting for GPS fix...")
    lat, lon = get_gps_coordinates(timeout=30)

    if lat and lon:
        link = build_google_maps_link(lat, lon)
        print(f"Latitude : {lat}")
        print(f"Longitude: {lon}")
        print(f"Maps Link: {link}")
    else:
        print("Could not get GPS fix. Check antenna and signal.")
