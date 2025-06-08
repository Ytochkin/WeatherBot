import json
import os

USER_DATA_FILE = 'storage/user_data.json'

try:
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            user_data = json.load(f)
    else:
        user_data = {}
except (FileNotFoundError, json.JSONDecodeError):
    user_data = {}

def save_user_data():
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f, indent=2)
