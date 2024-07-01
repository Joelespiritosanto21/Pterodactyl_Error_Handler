import json
import os

CONFIG_FILE = 'config.json'

default_config = {
    "panel_url": "http://localhost:port",
    "check_interval": 60,
    "service_name": "jexactyl_service_name",
    "wing_name": "wing_service_name",
    "recipient_emails": ["admin@example.com"],
    "sender_email": "monitor@example.com",
    "smtp_server": "smtp.example.com",
    "smtp_port": 465,
    "email_password": "your_email_password"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(default_config)
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Initialize configuration on first run
load_config()
