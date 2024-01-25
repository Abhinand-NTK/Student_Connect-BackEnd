# your_app/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from celery.utils.log import get_logger
import time

logger = get_logger(__name__)

@shared_task
def send_email_to_users(user_emails):
    try:
        logger.info("Sending email")
        # Your asynchronous task logic goes here
        subject = "New Video Study Materials Available"
        message = (
            f"Dear students,\n\n"
            f"We are excited to inform you that new Video Study Materials have been added to the course.\n"
            f"Subject: {subject}\n"
            f"Please find the materials available at the following link:\n"
            f"https://yourwebsite.com/study-materials\n\n"
            f"We encourage you to watch them as soon as possible to stay up-to-date with the course content.\n"
            f"Happy learning!\n\n"
            f"Best regards,\n"
            f"Your School/Institution Name"
        )
        send_mail(
            subject, message, "studentconnectweb@gmail.com", user_emails, fail_silently=True
        )
        logger.info("Email sent successfully")
        return "Task completed"
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise
