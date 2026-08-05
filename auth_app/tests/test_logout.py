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
        self.token = account_activation_token.make_token(self.user)
    
    def test_Logout_Happy(self):
        self.client.cookies['access_token'] = str(RefreshToken.for_user(self.user).access_token)
        url = reverse('logout')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.cookies['access_token'].value, "")
        self.assertEqual(response.cookies['refresh_token'].value, "")
        self.assertEqual(response.data['detail'],"Logout successful! All tokens will be deleted. Refresh token is now invalid.")

    def test_Logout_Unhappy_401(self):
        url = reverse('logout')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'],"Refresh-Token is missing.")
