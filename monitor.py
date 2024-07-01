import time
import requests
import psutil
import smtplib
from subprocess import call
from email.mime.text import MIMEText
from config_manager import load_config

config = load_config()

def send_notification(message):
    msg = MIMEText(message)
    msg['Subject'] = "Jexactyl Monitor Alert"
    msg['From'] = config['sender_email']
    msg['To'] = ', '.join(config['recipient_emails'])

    try:
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port']) as server:
            server.login(config['sender_email'], config['email_password'])
            server.sendmail(config['sender_email'], config['recipient_emails'], msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

def check_service(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def restart_service(service):
    print(f"Restarting service: {service}")
    call(["systemctl", "restart", service])

def clear_cache():
    print("Clearing panel cache")
    call(["rm", "-rf", "/path/to/cache/*"])

def check_process(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return True
    return False

def monitor():
    if not check_service(config['panel_url']):
        print("Panel is not responding. Taking corrective actions.")
        send_notification("Jexactyl panel is not responding.")
        clear_cache()
        restart_service(config['service_name'])
        restart_service(config['wing_name'])
    else:
        print("Panel is functioning normally.")
    
    time.sleep(config['check_interval'])
    monitor()

if __name__ == "__main__":
    monitor()
