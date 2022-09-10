from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from celery import shared_task


@shared_task()
def send_contact_me_mail(name, subject, email, message, user_email):
    body = render_to_string(
        template_name="../templates/contact.html",
        context={
            "name": name,
            "email": email,
            "message": message,
        }
    )
    mail = EmailMessage(subject=subject, body=body, to=[user_email])
    mail.send()
