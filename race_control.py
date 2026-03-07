import requests
import os
import json

WEBHOOK_URL = os.environ["WEBHOOK_URL"]
API_URL = "https://api.openf1.org/v1/race_control?session_key=latest"

STATE_FILE = "last_id.txt"

# Letzte gespeicherte ID laden
try:
    with open(STATE_FILE, "r") as f:
        last_id = f.read().strip()
except:
    last_id = None

data = requests.get(API_URL).json()

if not data:
    exit()

latest = data[-1]
current_id = latest["date"] + latest["message"]

if current_id != last_id:
    message = f"🚦 **{latest.get('category','Race Control')}**\n{latest['message']}"
    requests.post(WEBHOOK_URL, json={"content": message})

    with open(STATE_FILE, "w") as f:
        f.write(current_id)
