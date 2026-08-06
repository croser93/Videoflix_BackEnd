from rest_framework.test import APITestCase
from auth_app.models import CustomUser
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from auth_app.utils import encode_uid, account_activation_token

class PasswordResetTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@gmx.de', password='123456')
        self.user.is_active = True
        self.user.save()

    def test_password_reset_email_happy(self):
        url = reverse('password_reset')
        data ={
            'email': 'test@gmx.de'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'An email has been sent to reset your password.')

    def test_password_reset_email_invalid_email(self):
        url = reverse('password_reset')
        data ={
            'email': 9999
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid Email.')

    def test_password_reset_with_not_exist_email_(self):
        url = reverse('password_reset')
        data ={
            'email': 'unknow@gmx.de'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'An email has been sent to reset your password.')

    
    def test_password_reset_with_no_email_(self):
        url = reverse('password_reset')
        data ={

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
