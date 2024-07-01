from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

CONFIG_FILE = 'config.json'

def load_config():
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)

def save_config(config):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file, indent=4)

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/update', methods=['POST'])
def update_config():
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

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        initial_config = {
            'panel_url': '',
            'check_interval': 60,
            'service_name': '',
            'wing_name': '',
            'recipient_emails': [],
            'sender_email': '',
            'smtp_server': '',
            'smtp_port': 587,
            'email_password': ''
        }
        save_config(initial_config)
    app.run(debug=True)
