#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import requests
import smtplib
from email.mime.text import MIMEText

# --- CONFIG ---
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
CHECK_INTERVAL = 600  # seconds
THRESHOLD = 1  # % change
EMAIL_FROM = "@gmail.com"
EMAIL_TO = ""
EMAIL_PASSWORD = ""  # Use App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- FUNCTIONS ---
def get_eth_price():
    response = requests.get(API_URL)
    return response.json()["ethereum"]["usd"]

def send_email(subject, body):
    msg = MIMEText(body)
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

# --- MAIN LOOP ---
last_price = get_eth_price()
print(f"Starting ETH price monitor... Current price: ${last_price}")

while True:
    time.sleep(CHECK_INTERVAL)
    new_price = get_eth_price()
    change = (new_price - last_price) / last_price

    if abs(change) >= THRESHOLD:
        direction = "UP" if change > 0 else "DOWN"
        subject = f"🚨 ETH Price Alert: {direction} {change:.2%}"
        body = f"ETH price changed from ${last_price:.2f} to ${new_price:.2f} ({change:.2%})"
        print(subject, body)
        send_email(subject, body)

    last_price = new_price


# In[ ]:




