from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import base64
import django_rq

url = 'http://127.0.0.1:4000'

def send_activation_email(email, uid, token):
    """Render and enqueue the account activation email for asynchronous sending."""

    uid_token_link = f"{url}/pages/auth/activate.html?uid={uid}&token={token}"

    with open("auth_app/static/logo.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode("utf-8") 

    html_content = render_to_string(
    "activations_email.html",
    context={"link": uid_token_link, "email": email, "logo": logo_base64, 'url': url},
    )

    msg = EmailMultiAlternatives(
        subject="Confirm your email",
        body=html_content,
        from_email="info@Videoflix.com",
        to=[email],
        headers={"List-Unsubscribe": "<info@Videoflix.com>"},
    )
    msg.attach_alternative(html_content, "text/html")
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(msg.send)


    
def send_password_reset_mail(email, uid, token):
    """Render and enqueue the password reset email for asynchronous sending."""

    uid_token_link = f"{url}/pages/auth/confirm_password.html?uid={uid}&token={token}"
    
    with open("auth_app/static/logo.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode("utf-8") 

    html_content = render_to_string(
    "reset_password_email.html",
    context={"link": uid_token_link, "email": email, "logo": logo_base64},
    )

    msg = EmailMultiAlternatives(
        subject="Reset your Password",
        body=html_content,
        from_email="info@Videoflix.com",
        to=[email],
        headers={"List-Unsubscribe": "<info@Videoflix.com>"},
    )
    msg.attach_alternative(html_content, "text/html")
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(msg.send)