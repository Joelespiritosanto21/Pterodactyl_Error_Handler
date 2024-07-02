import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QPlainTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import requests
import time
from web_app import start_web_server

class MonitorThread(QThread):
    log_signal = pyqtSignal(str)

    def run(self):
        while True:
            try:
                response = requests.get('http://127.0.0.1:5000/logs')
                if response.status_code == 200:
                    logs = response.json().get('logs', '')
                    self.log_signal.emit(logs)
            except Exception as e:
                self.log_signal.emit(f"Error fetching logs: {e}")
            time.sleep(5)

class MonitorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jexactyl Monitor")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.start_monitor_button = QPushButton("Start Monitor")
        self.start_monitor_button.clicked.connect(self.start_monitor)
        self.layout.addWidget(self.start_monitor_button)

        self.stop_monitor_button = QPushButton("Stop Monitor")
        self.stop_monitor_button.clicked.connect(self.stop_monitor)
        self.layout.addWidget(self.stop_monitor_button)

        self.start_web_button = QPushButton("Start Web Server")
        self.start_web_button.clicked.connect(self.start_web_server)
        self.layout.addWidget(self.start_web_button)

        self.clear_console_button = QPushButton("Clear Console")
        self.clear_console_button.clicked.connect(self.clear_console)
        self.layout.addWidget(self.clear_console_button)

        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.layout.addWidget(self.console)

        self.monitor_thread = MonitorThread()
        self.monitor_thread.log_signal.connect(self.update_console)

    def start_monitor(self):
        self.monitor_thread.start()

    def stop_monitor(self):
        self.monitor_thread.terminate()

    def start_web_server(self):
        self.web_server_thread = threading.Thread(target=start_web_server)
        self.web_server_thread.start()

    def clear_console(self):
        self.console.clear()

    def update_console(self, logs):
        self.console.setPlainText(logs)
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())

def start_gui():
    app = QApplication(sys.argv)
    window = MonitorGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start_gui()
