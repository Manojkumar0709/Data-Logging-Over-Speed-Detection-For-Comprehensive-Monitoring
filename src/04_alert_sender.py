# ============================================================
# FILE: 04_alert_sender.py
# PURPOSE: Send email and SMS alerts when acceleration
#          exceeds the configured threshold
# LIBRARIES: smtplib (built-in), requests, python-dotenv
# ============================================================
# SETUP:
#   - For EMAIL: Use a Gmail account with App Password
#       (Enable 2FA on Google, then generate an App Password)
#   - For SMS: Create account at https://www.fast2sms.com
#       and get your API key
#   - Store all credentials in the .env file (never hardcode!)
# ============================================================

import smtplib                             # Built-in Python library for email
from email.mime.text import MIMEText       # For formatting plain text emails
from email.mime.multipart import MIMEMultipart  # For multi-part email structure
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Load credentials from .env

# ---- Email credentials (from .env) ----
EMAIL_SENDER   = os.getenv("EMAIL_SENDER")    # Your Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Gmail App Password
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")  # Alert destination email

# ---- SMS credentials (from .env) ----
FAST2SMS_API_KEY    = os.getenv("FAST2SMS_API_KEY")
FAST2SMS_PHONE      = os.getenv("ALERT_PHONE_NUMBER")  # 10-digit phone number


def send_email_alert(net_accel, maps_link):
    """
    Send an email alert with acceleration value, timestamp,
    and Google Maps link.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Build the email message ---
    msg = MIMEMultipart()
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = EMAIL_RECEIVER
    msg["Subject"] = "⚠️ ALERT: Over-Acceleration Detected!"

    body = (
        f"An over-acceleration event was detected.\n\n"
        f"Timestamp       : {timestamp}\n"
        f"Net Acceleration: {net_accel:.2f} m/s²\n"
        f"Location        : {maps_link}\n\n"
        f"Please check the vehicle/device immediately."
    )
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail's SMTP server (port 587 = TLS)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()                            # Upgrade connection to TLS
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Authenticate
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("Email alert sent successfully.")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_sms_alert(net_accel, maps_link):
    """
    Send an SMS alert via Fast2SMS API.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    message = (
        f"ALERT! Acceleration {net_accel:.2f} m/s² at {timestamp}. "
        f"Location: {maps_link}"
    )

    # Fast2SMS API endpoint and headers
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {"authorization": FAST2SMS_API_KEY}
    payload = {
        "route"   : "q",                  # Quick SMS route
        "message" : message,
        "language": "english",
        "flash"   : 0,
        "numbers" : FAST2SMS_PHONE,
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        result = response.json()
        if result.get("return") is True:
            print("SMS alert sent successfully.")
            return True
        else:
            print(f"SMS failed: {result}")
            return False
    except Exception as e:
        print(f"SMS error: {e}")
        return False


# ---- STANDALONE TEST ----
if __name__ == "__main__":
    print("Alert Sender Test")
    test_link = "https://maps.google.com/?q=12.9716,77.5946"
    send_email_alert(net_accel=12.5, maps_link=test_link)
    send_sms_alert(net_accel=12.5, maps_link=test_link)
