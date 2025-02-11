# FreeFileSync Log & Email Notifier

## Overview
This repository contains a Python script (`sync_mail.py`) designed to automate **folder synchronization** using FreeFileSync and send email notifications containing synchronization logs. 

It is useful for maintaining up-to-date backups, monitoring changes in critical folders, and ensuring log tracking via email notifications.

---

## Features
- **Automated Folder Synchronization:** Uses FreeFileSync to sync folders based on predefined batch settings.
- **Log Generation:** Automatically creates HTML log files recording sync operations.
- **Email Notifications:** Sends an email with the latest sync log attached, ensuring you are notified of sync results.
- **Folder Comparison:** Uses FreeFileSync metadata (`.sync.ffs_db`) to track and compare folder differences.

---

## Prerequisites
### Software Requirements
To use this script, ensure the following dependencies are installed:
- **Python 3.x** (Recommended: latest version)
- **FreeFileSync** (Must be installed at `/usr/local/bin/FreeFileSync` or adjusted in the script)
- **SMTP-enabled email account** (For sending log notifications)

### Python Dependencies
Before running the script, install the required Python modules using:
```bash
pip install smtplib email
```

---

## Setup & Usage
### 1. Configure FreeFileSync
- Open **FreeFileSync** and create a batch file (`.ffs_batch`).
- Set the source and destination folders for synchronization.
- Enable **logging** in FreeFileSync to generate HTML log files.
- Save the batch file for use with this script.

### 2. Run the Script
Once FreeFileSync is set up, run the script using:
```bash
python sync_mail.py
```

### 3. How It Works
1. The script executes **FreeFileSync** using the specified batch job.
2. It retrieves the latest log file from the `Logs/` directory.
3. It formats the log file and sends an email notification to specified recipients.

### 4. Email Configuration
Modify the script with your email credentials to enable email notifications:
```python
from_email = "your_email@example.com"
from_email_password = "your_password"
smtp_server = "smtp.example.com"
smtp_port = 587
to_emails = ["recipient@example.com"]
cc_emails = ["cc@example.com"]
```
> **Note:** For security reasons, consider using environment variables or encrypted storage for storing email credentials.

---

## Folder Comparison
- The script interacts with `Compare1/` and `Compare2/` folders.
- These folders store FreeFileSync metadata files (`.sync.ffs_db`), which track differences and sync changes.
- `Comandos.txt` files in these folders may contain additional synchronization instructions or logs.

---

## Logs
- Sync logs are stored in the `Logs/` directory.
- Logs follow a structured naming format:
  ```
  sync_folders2 YYYY-MM-DD HHMMSS.XXX.html
  ```
- The logs contain:
  - **Timestamp** of synchronization.
  - **List of modified, added, and deleted files**.
  - **Errors encountered** (if any).

---

## Screenshot
To visualize how the email notifications appear, see the screenshot below:

![Email Notification](e-mail_received.png)

---

## Automation
To automate the script execution, set up a scheduled task:

### **Linux/macOS (Using Cron Jobs)**
Run the script daily at midnight:
```bash
0 0 * * * /usr/bin/python3 /path/to/sync_mail.py
```

### **Windows (Using Task Scheduler)**
1. Open **Task Scheduler**.
2. Create a new task.
3. Set the trigger to run **daily** or as per your schedule.
4. Set the action to execute `python sync_mail.py`.

---

## Troubleshooting
### 1. FreeFileSync Not Found Error
- Ensure FreeFileSync is installed and accessible at `/usr/local/bin/FreeFileSync`.
- Modify the script to use the correct path if necessary.

### 2. Email Not Sent
- Verify SMTP credentials and server details.
- Check for firewall or security restrictions preventing email sending.
- Enable **"Less Secure Apps"** access if using Gmail (not recommended for security reasons).

---
