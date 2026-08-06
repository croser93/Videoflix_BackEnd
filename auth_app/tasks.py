
def send_activation_email(email, uid, token):
    print(f"Aktivierungslink für {email} : /activate/{uid}/{token}/")

def send_password_reset_mail(email, uid, token):
    print(f"Reset Link für  {email} : /reset_password/{uid}/{token}/")