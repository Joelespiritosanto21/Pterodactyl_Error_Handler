import json
import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def send_email(subject, body, config):
    msg = MIMEMultipart()
    msg['From'] = config['sender_email']
    msg['To'] = ", ".join(config['recipient_emails'])
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
        server.starttls()
        server.login(config['sender_email'], config['email_password'])
        server.send_message(msg)

def check_status(config):
    try:
        response = requests.get(config['panel_url'])
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking status: {e}")
        return False

def clear_cache(config):
    try:
        response = requests.get(f"{config['panel_url']}/api/clear-cache", headers={'Authorization': f"Bearer {config['api_token']}"})
        return response.status_code == 200
    except Exception as e:
        print(f"Error clearing cache: {e}")
        return False

def restart_services(config):
    try:
        response = requests.get(f"{config['panel_url']}/api/restart", headers={'Authorization': f"Bearer {config['api_token']}"})
        return response.status_code == 200
    except Exception as e:
        print(f"Error restarting services: {e}")
        return False

def main():
    config = load_config()
    while True:
        if not check_status(config):
            send_email('Jexactyl Panel Down', 'The Jexactyl panel is not responding. Attempting to clear cache and restart services.', config)
            if clear_cache(config) and restart_services(config):
                send_email('Jexactyl Services Restarted', 'The Jexactyl panel services have been successfully restarted.', config)
            else:
                send_email('Jexactyl Services Restart Failed', 'Failed to restart Jexactyl panel services.', config)
        time.sleep(config['check_interval'])

if __name__ == "__main__":
    main()
