from rest_framework.test import APITestCase
from auth_app.models import CustomUser
from django.urls import reverse
from rest_framework import status
from auth_app.utils import encode_uid
from django.contrib.auth.tokens import default_token_generator


class PasswordConfirmTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@gmx.de', password='123456')
        self.user.is_active = True
        self.user.save()
        self.uid = encode_uid(self.user)
        

    def test_password_confirm_happy(self):
        self.token = default_token_generator.make_token(self.user)
        url = reverse('password_confirm',  args=[self.uid, self.token])
        data = {
                "new_password": "newsecurepassword",
                "confirm_password": "newsecurepassword"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Your Password has been successfully reset.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(data['new_password']))

    def test_password_confirm_invalid_token(self):
        self.token = 'invalid Token'
        url = reverse('password_confirm',  args=[self.uid, self.token])
        data = {
                "new_password": "newsecurepassword",
                "confirm_password": "newsecurepassword"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token is invalid.')

    def test_password_confirm_pw_dont_match(self):
        self.token = default_token_generator.make_token(self.user)
        url = reverse('password_confirm',  args=[self.uid, self.token])
        data = {
                "new_password": "newsecurepassword",
                "confirm_password": "newsecurepassword99999"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'password dont match.')

    def test_password_confirm_token_reused_after_reset(self):
        self.token = default_token_generator.make_token(self.user)
        url = reverse('password_confirm', args=[self.uid, self.token])
        data = {
            "new_password": "newsecurepassword",
            "confirm_password": "newsecurepassword"
        }
        self.client.post(url, data)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


