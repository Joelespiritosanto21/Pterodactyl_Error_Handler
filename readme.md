# Jexactyl Monitor

This project provides a monitoring system for Jexactyl, including a GUI for local management and a web portal for remote access and configuration.

## Features

- **Monitoring**: Continuously checks the status of the Jexactyl panel and services.
- **Alerts**: Sends email notifications when issues are detected.
- **Automatic Actions**: Clears panel cache and restarts services upon failure.
- **GUI**: Local interface using Tkinter for easy setup and control.
- **Web Portal**: Remote configuration and monitoring via Flask-based web application.
- **Configuration**: Settings stored in a JSON file (`config.json`).

## Setup Instructions

### Prerequisites

- Python 3.6 or higher installed.
- Pip package manager.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/jexactyl-monitor.git
    cd jexactyl-monitor
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. **Config.json**

    - Modify `config.json` to specify:
        - `panel_url`: URL of the Jexactyl panel.
        - `check_interval`: Interval (in seconds) between each status check.
        - `service_name`: Name of the Jexactyl service.
        - `wing_name`: Name of the Jexactyl wing service.
        - `recipient_emails`: Email addresses for receiving notifications (comma-separated).
        - `sender_email`: Email address for sending notifications.
        - `smtp_server`: SMTP server for email notifications.
        - `smtp_port`: SMTP server port.
        - `email_password`: Password for the sender email account.

### Usage

#### 1. Start the Monitor

Run the monitor script (`monitor.py`):

```bash
python monitor.py
```

# Local GUI (Optional)
##I f you prefer a graphical interface for local management:
```bash
python gui.py
```
This will open a Tkinter-based GUI where you can start monitoring and perform service restarts.

# Web Portal (Optional)
## For remote configuration and monitoring via a web interface:
```bash
python web_app.py
```
Access the web interface at http://localhost:5000 (this is the defautl port, can be changed) to view status, restart services, and update settings.

# Contributing
## Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

# License
## This project is licensed under the MIT License - see the LICENSE file for details.


## Important Notes:

- **Prerequisites**: Make sure Python and Pip are installed before proceeding.
- **Installation**: Instructions to clone the repository and install necessary dependencies.
- **Configuration**: Guidance on configuring the `config.json` file with specific details for your Jexactyl environment.
- **Usage**: Clear instructions on how to start monitoring, use the local GUI (if desired), and access the web portal for remote configuration.
- **Contributions**: Encouragement for other developers to contribute to the project.
- **License**: Information about the project's license for transparency and legal compliance.

This README.md will provide users with all the necessary information to understand, install, configure, and effectively use your Jexactyl monitoring project. Be sure to update it as needed to reflect any future changes or additions to the project.
