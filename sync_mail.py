import subprocess
import smtplib
import os
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function to run FreeFileSync batch job
def run_free_file_sync(batch_file_path):
    try:
        # Run FreeFileSync with logging already set in the batch file
        result = subprocess.run(['/usr/local/bin/FreeFileSync', batch_file_path], check=True)
        return True, "FreeFileSync job completed successfully."
    except subprocess.CalledProcessError as e:
        return False, f"Error running FreeFileSync job: {e}"


# Function to send an email with CC
def send_email(subject, html_body, to_emails, cc_emails, from_email, from_email_password, smtp_server, smtp_port):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(to_emails)
        msg['Cc'] = ', '.join(cc_emails)
        msg['Subject'] = subject
        
        # Attach the HTML body
        msg.attach(MIMEText(html_body, 'html'))
        
        # Combine 'To' and 'Cc' emails for sending
        all_recipients = to_emails + cc_emails
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_email_password)
        text = msg.as_string()
        server.sendmail(from_email, all_recipients, text)
        server.quit()
        
        return True, "Email sent successfully."
    except Exception as e:
        return False, f"Error sending email: {e}"


# Function to find the latest log file in a directory
def get_latest_log_file(directory, extension="html"):
    """
    Finds the latest file in the specified directory with the given extension.
    """
    try:
        # Find all files with the specified extension
        files = glob.glob(f"{directory}/*.{extension}")
        # Return the newest file based on creation time
        latest_file = max(files, key=os.path.getctime)
        return latest_file
    except ValueError:  # No files found
        return None


# Function to read HTML log file
def read_log_file(log_file_path):
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            return file.read()  # Read the content of the HTML log file
    else:
        return "<p>Log file not found.</p>"


# Main function to run FreeFileSync and send email
def main():
    # Paths and configuration
    batch_file_path = "sync_folders2.ffs_batch"
    log_directory = "/Logs"  # Replace with your logs directory
    
    # Email credentials
    from_email = "e-mail@yahoo.com.br"
    from_email_password = "password"  # Replace with your email password or use environment variables
    to_emails = ["email1@gmail.com"]
    cc_emails = ["email2@gmail.com"]
    
    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587

    # Run the FreeFileSync batch job
    success, message = run_free_file_sync(batch_file_path)

    # Find the latest log file dynamically
    log_file_path = get_latest_log_file(log_directory)

    # Prepare email content
    if log_file_path:
        log_content = read_log_file(log_file_path)
    else:
        log_content = "<p>No logs found in the specified directory.</p>"

    if success:
        subject = "FreeFileSync Job Success"
        html_body = f"<p>The FreeFileSync job completed successfully.</p><h3>Log report:</h3>{log_content}"
    else:
        subject = "FreeFileSync Job Failed"
        html_body = f"<p>The FreeFileSync job failed with the following error:</p><p>{message}</p>"

    # Send the email
    email_success, email_message = send_email(
        subject, html_body, to_emails, cc_emails, from_email, from_email_password, smtp_server, smtp_port
    )
    
    # Print results
    print(message)
    print(email_message)


if __name__ == "__main__":
    main()
