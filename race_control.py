import requests
import os
import json

API_URL = "https://api.openf1.org/v1/race_control?session_key=latest"
WEBHOOK = os.environ["WEBHOOK_URL"]

STATE_FILE = "last_timestamp.txt"

# letzte verarbeitete Zeit laden
try:
    with open(STATE_FILE, "r") as f:
        last_time = f.read().strip()
except:
    last_time = ""

data = requests.get(API_URL).json()

new_last_time = last_time

for item in data:

    timestamp = item["date"]

    if timestamp <= last_time:
        continue

    category = item.get("category", "Race Control")
    message = item.get("message", "")

    color = 8421504

    cat = category.upper()

    if "RED" in cat:
        color = 16711680
    elif "YELLOW" in cat:
        color = 16776960
    elif "SAFETY" in cat:
        color = 16753920
    elif "GREEN" in cat:
        color = 65280

    embed = {
        "title": category,
        "description": message,
        "color": color
    }

    payload = {
        "embeds": [embed]
    }

    requests.post(WEBHOOK, json=payload)

    new_last_time = timestamp

# neue letzte Zeit speichern
with open(STATE_FILE, "w") as f:
    f.write(new_last_time)
