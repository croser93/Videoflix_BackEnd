from rest_framework.test import APITestCase
from auth_app.models import CustomUser
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from auth_app.utils import encode_uid, account_activation_token

class LogoutTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@gmx.de', password='123456')
        self.uid = encode_uid(self.user)
        self.user.is_active = True
        self.user.save()
        

    def test_refresh_happy(self):
        self.token = account_activation_token.make_token(self.user)
        self.client.cookies['refresh_token'] = str(RefreshToken.for_user(self.user))
        url = reverse('token_refresh')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Token refreshed")
        self.assertEqual(response.data['access'], response.cookies['access_token'].value)
        self.assertIn('access_token', response.cookies)

    def test_refresh_unhappy_401(self):
        self.client.cookies['refresh_token'] = 'invalid token'
        url = reverse('token_refresh')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Refresh token is invalid.")

    def test_refresh_unhappy_400(self):
        url = reverse('token_refresh')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Refresh token is missing.")