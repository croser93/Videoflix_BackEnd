from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from auth_app.models import CustomUser
from django.urls import reverse
from rest_framework import status

class RegistrationTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test1@gmx.de', password="123456")


    def test_registration_happy(self):
        url = reverse('register')
        data = {
            'email': "test@gmx.de",
            'password': "123456",
            "confirmed_password": "123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(response.data['user'], response.data['user'])

    def test_registration_400(self):
        url = reverse('register')
        data = {
            'password': "123456",
            "confirmed_password": "123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_registration_email_exist(self):
        url = reverse('register')
        data = {
            'email': "test1@gmx.de",
            'password': "123456",
            "confirmed_password": "123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'email exist')
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_registration_pw_dont_match(self):
        url = reverse('register')
        data = {
            'email': "test@gmx.de",
            'password': "123456",
            "confirmed_password": "99999999"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'password dont match')
        self.assertEqual(CustomUser.objects.count(), 1)
