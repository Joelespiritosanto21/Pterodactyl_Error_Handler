import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(config, subject, body):
    msg = MIMEMultipart()
    msg['From'] = config['sender_email']
    msg['To'] = ", ".join(config['recipient_emails'])
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['sender_email'], config['email_password'])
            server.send_message(msg)
        log_message("Email sent successfully.")
    except Exception as e:
        log_message(f"Failed to send email: {e}")

def restart_services(config):
    log_message("Restarting Jexactyl services...")
    subject = "Jexactyl Services Restarted"
    body = "The Jexactyl services were restarted due to an error or unresponsive state."
    send_email(config, subject, body)

def check_jexactyl_status(config):
    while True:
        try:
            response = requests.get(config['panel_url'])
            if response.status_code == 200:
                log_message("Jexactyl is running smoothly.")
            else:
                log_message("Jexactyl seems to be having issues.")
                restart_services(config)
        except requests.RequestException as e:
            log_message(f"Error connecting to Jexactyl: {e}")
            restart_services(config)
        time.sleep(config.get('check_interval', 60))

def start_monitoring(config):
    log_message("Monitoring started.")
    check_jexactyl_status(config)

def log_message(message):
    with open('monitor.log', 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
