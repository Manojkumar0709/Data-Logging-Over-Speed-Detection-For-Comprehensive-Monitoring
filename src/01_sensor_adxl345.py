# ============================================================
# FILE: 01_sensor_adxl345.py
# PURPOSE: Read acceleration data from the ADXL345 sensor
# INTERFACE: I2C (connected to Raspberry Pi GPIO pins 3 & 5)
# LIBRARY: adafruit-circuitpython-adxl34x
# ============================================================
# HARDWARE CONNECTIONS (ADXL345 --> Raspberry Pi Zero WH)
#   VCC  --> 3.3V  (Pin 1)
#   GND  --> GND   (Pin 6)
#   SDA  --> GPIO2 (Pin 3)  -- I2C Data
#   SCL  --> GPIO3 (Pin 5)  -- I2C Clock
# ============================================================

import board          # Provides board pin definitions for Raspberry Pi
import busio          # Provides I2C/SPI communication protocols
import adafruit_adxl34x  # Adafruit library for ADXL345 sensor
import time

# --- Step 1: Initialize the I2C bus ---
# 'board.SCL' and 'board.SDA' refer to the hardware I2C pins on the Pi
i2c = busio.I2C(board.SCL, board.SDA)

# --- Step 2: Create the sensor object ---
# This tells the library which sensor is connected on the I2C bus
accelerometer = adafruit_adxl34x.ADXL345(i2c)


def read_raw_acceleration():
    """
    Read a single (x, y, z) acceleration reading from the sensor.
    Returns values in m/s².
    """
    x, y, z = accelerometer.acceleration
    return x, y, z


def read_averaged_acceleration(samples=5):
    """
    Take multiple readings and average them to reduce sensor noise.
    'samples' = how many readings to average (default: 5)
    Returns averaged (x, y, z) in m/s².
    """
    x_total, y_total, z_total = 0.0, 0.0, 0.0

    for _ in range(samples):
        x, y, z = accelerometer.acceleration
        x_total += x
        y_total += y
        z_total += z
        time.sleep(0.05)  # Small delay between readings

    x_avg = x_total / samples
    y_avg = y_total / samples
    z_avg = z_total / samples

    return x_avg, y_avg, z_avg


def compute_net_acceleration(x, y, z):
    """
    Compute the magnitude of the 3D acceleration vector,
    then subtract gravity (9.8 m/s²) to get net dynamic acceleration.

    Formula: magnitude = sqrt(x² + y² + z²)
    Net acceleration = magnitude - 9.8
    """
    import math
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    net_accel = magnitude - 9.8  # Remove the constant gravity component
    return net_accel


# ---- STANDALONE TEST ----
# Run this file directly to test sensor readings
if __name__ == "__main__":
    print("ADXL345 Sensor Test --- Press Ctrl+C to stop")
    print("-" * 45)
    while True:
        x, y, z = read_averaged_acceleration(samples=5)
        net = compute_net_acceleration(x, y, z)
        print(f"X: {x:.2f}  Y: {y:.2f}  Z: {z:.2f}  |  Net Accel: {net:.2f} m/s²")
        time.sleep(1)
