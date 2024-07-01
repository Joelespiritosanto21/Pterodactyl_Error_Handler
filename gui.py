import sys
import json
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTabWidget, QFormLayout, QLineEdit, QSpinBox
from PyQt5.QtGui import QIntValidator
from monitor import start_monitoring
from web_app import start_web_server

class MonitorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = self.load_config()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Jexactyl Monitor')

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.status_tab = QWidget()
        self.config_tab = QWidget()

        self.tabs.addTab(self.status_tab, "Status")
        self.tabs.addTab(self.config_tab, "Settings")

        self.init_status_tab()
        self.init_config_tab()

        self.show()

    def init_status_tab(self):
        layout = QVBoxLayout()

        self.status_label = QLabel('Status: Unknown', self)
        self.start_button = QPushButton('Start Monitoring', self)
        self.start_button.clicked.connect(self.start_monitoring)

        self.restart_button = QPushButton('Restart Services', self)
        self.restart_button.clicked.connect(self.restart_services)

        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.restart_button)

        self.status_tab.setLayout(layout)

    def init_config_tab(self):
        layout = QFormLayout()

        self.panel_url_input = QLineEdit(self.config.get('panel_url', ''))
        self.check_interval_input = QSpinBox()
        self.check_interval_input.setValue(self.config.get('check_interval', 60))
        self.service_name_input = QLineEdit(self.config.get('service_name', ''))
        self.wing_name_input = QLineEdit(self.config.get('wing_name', ''))
        self.recipient_emails_input = QLineEdit(','.join(self.config.get('recipient_emails', [])))
        self.sender_email_input = QLineEdit(self.config.get('sender_email', ''))
        self.smtp_server_input = QLineEdit(self.config.get('smtp_server', ''))
        self.smtp_port_input = QLineEdit(str(self.config.get('smtp_port', 587)))
        self.smtp_port_input.setValidator(QIntValidator(1, 999999))
        self.email_password_input = QLineEdit(self.config.get('email_password', ''))
        self.email_password_input.setEchoMode(QLineEdit.Password)

        save_button = QPushButton('Save Settings')
        save_button.clicked.connect(self.save_settings)

        layout.addRow('Panel URL:', self.panel_url_input)
        layout.addRow('Check Interval (seconds):', self.check_interval_input)
        layout.addRow('Service Name:', self.service_name_input)
        layout.addRow('Wing Name:', self.wing_name_input)
        layout.addRow('Recipient Emails:', self.recipient_emails_input)
        layout.addRow('Sender Email:', self.sender_email_input)
        layout.addRow('SMTP Server:', self.smtp_server_input)
        layout.addRow('SMTP Port:', self.smtp_port_input)
        layout.addRow('Email Password:', self.email_password_input)
        layout.addRow(save_button)

        self.config_tab.setLayout(layout)

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            return {}

    def save_config(self, config):
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)

    def start_monitoring(self):
        self.status_label.setText('Status: Monitoring...')
        monitor_thread = threading.Thread(target=start_monitoring, args=(self.config,))
        monitor_thread.start()

    def restart_services(self):
        try:
            response = requests.get(f"{self.config['panel_url']}/api/restart", headers={'Authorization': f"Bearer {self.config['api_token']}"})
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Services restarted successfully')
            else:
                QMessageBox.warning(self, 'Failed', 'Failed to restart services')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {e}")

    def save_settings(self):
        self.config['panel_url'] = self.panel_url_input.text()
        self.config['check_interval'] = self.check_interval_input.value()
        self.config['service_name'] = self.service_name_input.text()
        self.config['wing_name'] = self.wing_name_input.text()
        self.config['recipient_emails'] = self.recipient_emails_input.text().split(',')
        self.config['sender_email'] = self.sender_email_input.text()
        self.config['smtp_server'] = self.smtp_server_input.text()
        self.config['smtp_port'] = int(self.smtp_port_input.text())
        self.config['email_password'] = self.email_password_input.text()

        self.save_config(self.config)
        QMessageBox.information(self, 'Settings Saved', 'Your settings have been saved.')

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
    
    # Iniciar o monitoramento em uma thread separada
    monitor_thread = threading.Thread(target=start_monitoring, args=(config,))
    monitor_thread.start()

    # Iniciar o servidor Flask na thread principal
    flask_thread = threading.Thread(target=start_web_server)
    flask_thread.start()

    app = QApplication(sys.argv)
    ex = MonitorGUI()
    sys.exit(app.exec_())
