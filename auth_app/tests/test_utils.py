from django.test import TestCase
from auth_app.models import CustomUser
from auth_app.utils import encode_uid, get_user_from_uidb64, account_activation_token

class UtilTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email='test@gmx.de', password='123456')

    def test_token_is_Valid(self):
        token = account_activation_token.make_token(self.user)
        is_valid = account_activation_token.check_token(self.user, token)
        self.assertTrue(is_valid)

    def test_encode_uid_returns_string(self):
        uid = encode_uid(self.user)
        decoded_user = get_user_from_uidb64(uid)
        self.assertEqual(decoded_user, self.user)