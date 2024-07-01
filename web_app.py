from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

config_path = 'config.json'

def load_config():
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return {}

def save_config(config):
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def get_log_content():
    if os.path.exists('monitor.log'):
        with open('monitor.log', 'r') as log_file:
            return log_file.read()
    return "No logs available."

@app.route('/')
def index():
    config = load_config()
    logs = get_log_content()
    return render_template('index.html', config=config, logs=logs)

@app.route('/save', methods=['POST'])
def save():
    config = {
        'panel_url': request.form['panel_url'],
        'check_interval': int(request.form['check_interval']),
        'service_name': request.form['service_name'],
        'wing_name': request.form['wing_name'],
        'recipient_emails': request.form['recipient_emails'].split(','),
        'sender_email': request.form['sender_email'],
        'smtp_server': request.form['smtp_server'],
        'smtp_port': int(request.form['smtp_port']),
        'email_password': request.form['email_password']
    }
    save_config(config)
    return redirect(url_for('index'))

def start_web_server():
    # Use `0.0.0.0` se você precisa acessar a partir de outros dispositivos na rede
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    config = {
        'panel_url': 'http://your_jexactyl_url',
        'check_interval': 60,
        'service_name': 'jexactyl',
        'wing_name': 'jexactyl-wing',
        'recipient_emails': ['your_email@example.com'],
        'sender_email': 'your_sender_email@example.com',
        'smtp_server': 'your_smtp_server',
        'smtp_port': 587,
        'email_password': 'your_email_password'
    }
    save_config(config)

    # Iniciar o servidor Flask
    start_web_server()
