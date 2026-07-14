
## Tech Stack

| Layer | Technology |
|---|---|
| Hardware | Raspberry Pi Zero WH, ADXL345, GSM/GPRS/GPS module, HAT |
| Language | Python |
| Sensor Interface | I2C, Adafruit ADXL345 library |
| GPS Communication | UART/Serial (pyserial) |
| Cloud Logging | ThingSpeak (HTTP API) |
| Alerting | SMTP (email), Fast2SMS (SMS) |
| Enclosure Design | AutoCAD (3D modeling) |
| OS | Raspberry Pi OS (Linux) |

## How It Works

1. Initialize the ADXL345 sensor and GPS serial connection.
2. Continuously sample acceleration on X, Y, Z axes and average 5 readings to reduce noise.
3. Compute magnitude: `√(x² + y² + z²)`, then subtract 9.8 m/s² to isolate net (dynamic) acceleration.
4. Push the reading to ThingSpeak for live monitoring.
5. If net acceleration exceeds the configured threshold, fetch GPS coordinates, build a Google Maps link, and send an alert via email and SMS containing timestamp, acceleration value, and location.

## Testing & Validation

- Threshold testing at 5, 10, and 15 m/s² to tune sensitivity
- Verified real-time ThingSpeak data upload and visualization
- Verified email and SMS alert delivery with correct GPS link
- Boundary and stress testing under continuous acceleration input
- Extended runtime test (~3 hours) to confirm hardware stability

## Known Limitations

- Detects acceleration events, not vehicle speed directly — the term "overspeed" in early documentation was inaccurate and has been corrected here
- GPS/GSM connectivity affects alert reliability in low-signal areas
- Requires physical calibration and secure mounting for accurate readings
- Not a certified safety or legal-compliance device

## Future Improvements

- Replace GSM/GPRS with LTE module for more reliable connectivity
- Add local offline data buffering for network outages
- Build a dedicated dashboard instead of relying solely on ThingSpeak
- Add proper unit tests and CI for the Python codebase

## Setup

```bash
git clone https://github.com/Manojkumar0709/Data-Logging-Over-Speed-Detection-For-Comprehensive-Monitoring.git
cd Data-Logging-Over-Speed-Detection-For-Comprehensive-Monitoring
pip install -r requirements.txt
cp .env.example .env   # add your own ThingSpeak/SMTP/Fast2SMS credentials
python src/monitor.py
```

## Author

**Manoj Kumar Mohankumar**  
[LinkedIn](https://www.linkedin.com/in/manojkumar-m-93996714b/) · [GitHub](https://github.com/Manojkumar0709)
