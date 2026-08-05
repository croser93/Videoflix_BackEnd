from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from auth_app.models import CustomUser

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

def encode_uid(user):
    force_uid = force_bytes(user.id)
    base64 = urlsafe_base64_encode(force_uid)
    return base64

def get_user_from_uidb64(uidb64):
    try:
        base64_decode = urlsafe_base64_decode(uidb64)
        force_uid_decode = force_str(base64_decode)
        user = CustomUser.objects.get(pk=force_uid_decode)
        return user
    except:
        return None

account_activation_token = AccountActivationTokenGenerator()