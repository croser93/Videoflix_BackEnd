from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class RegistrationTest(APITestCase):

    def test_registration_happy(self):
        url = reverse('register')
        data = {
            'email': "test@gmx.de",
            'password': "123456",
            "confirmed_password": "123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_400(self):
        url = reverse('register')
        data = {
            'password': "123456",
            "confirmed_password": "123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)