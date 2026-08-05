from rest_framework.test import APITestCase
from auth_app.models import CustomUser
from django.urls import reverse
from rest_framework import status

class LoginTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@gmx.de', password='123456')
        self.user.is_active = True
        self.user.save()

    def test_login_happy(self):
        url = reverse('login')
        data = {
            'email': 'test@gmx.de',
            'password': '123456'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Login successfully!')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], self.user.email)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertIn('refresh_token', response.cookies)
        self.assertIn('access_token', response.cookies)

    def test_Login_Wrong_PW(self):
        url = reverse('login')
        data = {
            'email': 'test@gmx.de',
            'password':'test99999'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)