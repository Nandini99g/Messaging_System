from dotenv import load_dotenv
from celery import Celery
from datetime import datetime
import smtplib
import os
import logging

# Load environment variables from .env
load_dotenv()

# Configure Celery with RabbitMQ broker
celery = Celery('tasks', broker='pyamqp://guest@localhost//')

# Setup basic logging
logging.basicConfig(
    filename='celery_tasks.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Email task
@celery.task(bind=True)
def send_email_task(self, recipient):
    sender = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")

    if not sender or not password:
        logging.error("SMTP_USER or SMTP_PASSWORD not set in environment")
        raise ValueError("SMTP_USER or SMTP_PASSWORD not set!")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            message = f"Subject: Test Mail\n\nHello, this is a Celery + RabbitMQ test email!"
            server.sendmail(sender, recipient, message)
            logging.info(f"Email successfully sent to {recipient}")
        return f"Email sent to {recipient}"
    except smtplib.SMTPException as e:
        logging.error(f"Failed to send email to {recipient}: {e}")
        raise e

# Log time task
@celery.task(bind=True)
def log_time_task(self):
    try:
        with open("app.log", "a") as f:
            f.write(f"Current Time: {datetime.now()}\n")
        logging.info("Current time logged successfully")
        return "Time logged"
    except Exception as e:
        logging.error(f"Failed to log time: {e}")
        raise e
