from flask import Flask, render_template, request, redirect, url_for
from config_manager import load_config, save_config
from monitor import check_service, restart_service

app = Flask(__name__)

config = load_config()

@app.route('/')
def index():
    status = "Functioning" if check_service(config['panel_url']) else "Failed"
    return render_template('index.html', status=status)

@app.route('/restart')
def restart():
    restart_service(config['service_name'])
    restart_service(config['wing_name'])
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
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
    return render_template('settings.html', config=config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)