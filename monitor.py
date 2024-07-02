from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
import os
import threading

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

def clear_logs():
    if os.path.exists('monitor.log'):
        open('monitor.log', 'w').close()

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

@app.route('/logs')
def logs():
    logs = get_log_content()
    return jsonify({'logs': logs})

@app.route('/clear_logs', methods=['POST'])
def clear_logs_route():
    clear_logs()
    return jsonify({'status': 'Logs cleared'})

def start_web_server():
    app.run(debug=False, port=5000)

if __name__ == "__main__":
    start_web_server()
