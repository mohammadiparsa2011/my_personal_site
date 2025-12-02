# apps/core/tasks.py
from celery import shared_task

@shared_task
def send_contact_email_to_admin(contact_id):
    # اینجا فقط pass بگذاریم تا import موفق شود
    pass
