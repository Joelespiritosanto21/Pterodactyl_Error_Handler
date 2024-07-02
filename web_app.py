import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import threading

app = Flask(__name__)

CONFIG_FILE = 'config.json'
LOG_FILE = 'monitor.log'

logging.basicConfig(level=logging.DEBUG)

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

@app.route('/')
def index():
    try:
        config = load_config()
        return render_template('index.html', config=config)
    except Exception as e:
        app.logger.error(f"Error in index route: {e}")
        return "Internal Server Error", 500

@app.route('/save', methods=['POST'])
def save():
    try:
        config = load_config()
        config['panel_url'] = request.form['panel_url']
        config['check_interval'] = int(request.form['check_interval'])
        config['service_name'] = request.form['service_name']
        config['wing_name'] = request.form['wing_name']
        config['recipient_emails'] = request.form['recipient_emails'].split(',')
        config['sender_email'] = request.form['sender_email']
        config['smtp_server'] = request.form['smtp_server']
        config['smtp_port'] = int(request.form['smtp_port'])
        config['email_password'] = request.form['email_password']
        save_config(config)
        return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f"Error in save route: {e}")
        return "Internal Server Error", 500

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        with open(LOG_FILE, 'r') as file:
            logs = file.readlines()
        return jsonify({'logs': logs})
    except Exception as e:
        app.logger.error(f"Error in get_logs route: {e}")
        return "Internal Server Error", 500

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    try:
        with open(LOG_FILE, 'w') as file:
            file.write('')
        return jsonify({'status': 'Logs cleared'})
    except Exception as e:
        app.logger.error(f"Error in clear_logs route: {e}")
        return "Internal Server Error", 500

def start_web_server():
    app.run(debug=False, port=5000)

if __name__ == '__main__':
    start_web_server()
