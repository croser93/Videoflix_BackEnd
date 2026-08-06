from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_activation_email(email, uid, token):
    uid_token_link = f"/activate/{uid}/{token}/" 
    html_content = render_to_string(
    "activations_email.html",
    context={"link": uid_token_link},
    )
    
    msg = EmailMultiAlternatives(
        subject="Confirm your email",
        body=html_content,
        from_email="info@Videoflix.com",
        to=["to@example.com"],
        headers={"List-Unsubscribe": "<info@Videoflix.com>"},
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


    
def send_password_reset_mail(email, uid, token):
    print(f"Reset Link für  {email} : /reset_password/{uid}/{token}/")