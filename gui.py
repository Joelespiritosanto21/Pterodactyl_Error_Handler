import tkinter as tk
from tkinter import messagebox, ttk
from config_manager import load_config, save_config
from monitor import check_service, restart_service

config = load_config()

def start_monitoring():
    monitor()
    messagebox.showinfo("Monitoring", "Monitoring started")

def restart_services():
    restart_service(config['service_name'])
    restart_service(config['wing_name'])
    messagebox.showinfo("Services", "Services restarted")

def update_status():
    status = "Functioning" if check_service(config['panel_url']) else "Failed"
    status_label.config(text=f"Status: {status}")
    root.after(5000, update_status)

def save_settings():
    config['panel_url'] = panel_url_entry.get()
    config['check_interval'] = int(check_interval_entry.get())
    config['service_name'] = service_name_entry.get()
    config['wing_name'] = wing_name_entry.get()
    config['recipient_emails'] = recipient_emails_entry.get().split(',')
    config['sender_email'] = sender_email_entry.get()
    config['smtp_server'] = smtp_server_entry.get()
    config['smtp_port'] = int(smtp_port_entry.get())
    config['email_password'] = email_password_entry.get()
    save_config(config)
    messagebox.showinfo("Settings", "Settings saved successfully")

root = tk.Tk()
root.title("Jexactyl Monitor")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Monitor tab
monitor_frame = ttk.Frame(notebook, width=400, height=280)
monitor_frame.pack(fill='both', expand=True)

status_label = tk.Label(monitor_frame, text="Status: Unknown", font=("Arial", 14))
status_label.pack(pady=10)

start_button = tk.Button(monitor_frame, text="Start Monitoring", command=start_monitoring, font=("Arial", 12))
start_button.pack(pady=5)

restart_button = tk.Button(monitor_frame, text="Restart Services", command=restart_services, font=("Arial", 12))
restart_button.pack(pady=5)

# Settings tab
settings_frame = ttk.Frame(notebook, width=400, height=280)
settings_frame.pack(fill='both', expand=True)

panel_url_label = tk.Label(settings_frame, text="Panel URL")
panel_url_label.pack(pady=5)
panel_url_entry = tk.Entry(settings_frame)
panel_url_entry.pack(pady=5)
panel_url_entry.insert(0, config['panel_url'])

check_interval_label = tk.Label(settings_frame, text="Check Interval")
check_interval_label.pack(pady=5)
check_interval_entry = tk.Entry(settings_frame)
check_interval_entry.pack(pady=5)
check_interval_entry.insert(0, config['check_interval'])

service_name_label = tk.Label(settings_frame, text="Service Name")
service_name_label.pack(pady=5)
service_name_entry = tk.Entry(settings_frame)
service_name_entry.pack(pady=5)
service_name_entry.insert(0, config['service_name'])

wing_name_label = tk.Label(settings_frame, text="Wing Name")
wing_name_label.pack(pady=5)
wing_name_entry = tk.Entry(settings_frame)
wing_name_entry.pack(pady=5)
wing_name_entry.insert(0, config['wing_name'])

recipient_emails_label = tk.Label(settings_frame, text="Recipient Emails")
recipient_emails_label.pack(pady=5)
recipient_emails_entry = tk.Entry(settings_frame)
recipient_emails_entry.pack(pady=5)
recipient_emails_entry.insert(0, ','.join(config['recipient_emails']))

sender_email_label = tk.Label(settings_frame, text="Sender Email")
sender_email_label.pack(pady=5)
sender_email_entry = tk.Entry(settings_frame)
sender_email_entry.pack(pady=5)
sender_email_entry.insert(0, config['sender_email'])

smtp_server_label = tk.Label(settings_frame, text="SMTP Server")
smtp_server_label.pack(pady=5)
smtp_server_entry = tk.Entry(settings_frame)
smtp_server_entry.pack(pady=5)
smtp_server_entry.insert(0, config['smtp_server'])

smtp_port_label = tk.Label(settings_frame, text="SMTP Port")
smtp_port_label.pack(pady=5)
smtp_port_entry = tk.Entry(settings_frame)
smtp_port_entry.pack(pady=5)
smtp_port_entry.insert(0, config['smtp_port'])

email_password_label = tk.Label(settings_frame, text="Email Password")
email_password_label.pack(pady=5)
email_password_entry = tk.Entry(settings_frame, show='*')
email_password_entry.pack(pady=5)
email_password_entry.insert(0, config['email_password'])

save_button = tk.Button(settings_frame, text="Save Settings", command=save_settings, font=("Arial", 12))
save_button.pack(pady=10)

notebook.add(monitor_frame, text='Monitor')
notebook.add(settings_frame, text='Settings')

update_status()
root.mainloop()
