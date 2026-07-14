# 🚗 Data Logging & Over-Acceleration Detection System

> A Raspberry Pi–powered IoT solution for real-time acceleration monitoring, cloud logging, and instant alerting via Email & SMS.

![Python](https://img.shields.io/badge/Python-3-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red?logo=raspberrypi)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

## ✨ Overview

This system continuously monitors motion using an **ADXL345 accelerometer** connected to a **Raspberry Pi Zero WH**. When a sudden acceleration event crosses a set threshold, it instantly:

📍 Fetches the GPS location  
📧 Sends an email alert  
📱 Sends an SMS alert  
☁️ Logs live data to ThingSpeak for remote monitoring

Built as a hands-on IoT + embedded systems project combining **sensors, cloud APIs, and real-time alerting** — perfect for learners exploring hardware-software integration.

---

## 🧩 Tech Stack

| Layer | Technology |
|---|---|
| 🖥️ Hardware | Raspberry Pi Zero WH, ADXL345, GSM/GPRS/GPS module |
| 🐍 Language | Python |
| 🔗 Sensor Interface | I2C, Adafruit ADXL345 library |
| 📡 GPS Communication | UART/Serial (pyserial) |
| ☁️ Cloud Logging | ThingSpeak (HTTP API) |
| 🚨 Alerting | SMTP (Email), Fast2SMS (SMS) |
| 🧱 Enclosure | AutoCAD 3D Design |
| 💻 OS | Raspberry Pi OS (Linux) |

---

## ⚙️ How It Works

1️⃣ Initialize the ADXL345 sensor and GPS serial connection  
2️⃣ Continuously sample X, Y, Z acceleration and average readings to reduce noise  
3️⃣ Compute magnitude → `√(x² + y² + z²)` and subtract gravity (9.8 m/s²)  
4️⃣ Push live data to ThingSpeak  
5️⃣ If threshold exceeded → fetch GPS → build map link → send Email + SMS alert 🚨

---

## 📂 Repository Structure
├── README.md
├── Report.pdf
├── requirements.txt
├── .env.example
└── src/
├── 01_sensor_adxl345.py
├── 02_gps_reader.py
├── 03_thingspeak_logger.py
├── 04_alert_sender.py
└── 05_monitor.py

---

## 🚀 Quick Start

```bash
git clone https://github.com/Manojkumar0709/Data-Logging-Over-Speed-Detection-For-Comprehensive-Monitoring.git
cd Data-Logging-Over-Speed-Detection-For-Comprehensive-Monitoring
pip install -r requirements.txt
cp .env.example .env   # 🔑 add your ThingSpeak/SMTP/Fast2SMS credentials
python src/05_monitor.py
```

---

## ✅ Testing & Validation

- 🎯 Threshold testing at 5, 10, and 15 m/s²
- ☁️ Verified real-time ThingSpeak upload
- 📧📱 Verified Email + SMS alert delivery with GPS link
- 🔁 3-hour extended runtime stability test

---

## ⚠️ Known Limitations

- Detects acceleration events — not literal vehicle speed
- GPS/GSM reliability depends on signal strength
- Requires calibration & secure mounting
- Educational prototype, not a certified safety device

---

## 🔮 Future Improvements

- 📶 Upgrade GSM/GPRS to LTE
- 💾 Add offline data buffering
- 📊 Build a custom dashboard
- 🧪 Add unit tests & CI pipeline

---

## 👤 Author

**Manoj Kumar Mohankumar**  
[🔗 LinkedIn](https://www.linkedin.com/in/manojkumar-m-93996714b/) · [🐙 GitHub](https://github.com/Manojkumar0709)

