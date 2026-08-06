from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from auth_app.models import CustomUser
import base64

def send_activation_email(email, uid, token):
    uid_token_link = f"/activate/{uid}/{token}/" 

    with open("auth_app/static/logo.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode("utf-8") 

    html_content = render_to_string(
    "activations_email.html",
    context={"link": uid_token_link, "email": email, "logo": logo_base64},
    )

    msg = EmailMultiAlternatives(
        subject="Confirm your email",
        body=html_content,
        from_email="info@Videoflix.com",
        to=[email],
        headers={"List-Unsubscribe": "<info@Videoflix.com>"},
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


    
def send_password_reset_mail(email, uid, token):
    print(f"Reset Link für  {email} : /reset_password/{uid}/{token}/")