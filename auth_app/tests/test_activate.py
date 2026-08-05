from rest_framework.test import APITestCase
from auth_app.models import CustomUser
from django.urls import reverse
from rest_framework import status
from auth_app.utils import encode_uid, account_activation_token

class ActivateUser(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@gmx.de', password='123456')
        self.uid = encode_uid(self.user)
        self.token = account_activation_token.make_token(self.user)

    def test_activate_user_happy(self):
        url = reverse('acivate_token', args=[self.uid, self.token])
        self.assertFalse(self.user.is_active)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_user_is_aktiv(self):
        url = reverse('acivate_token', args=[self.uid, self.token])

        self.user.is_active = True
        self.user.save()

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_activate_user_uid_invalid(self):
        url = reverse('acivate_token', args=['9999', self.token])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_user_token_invalid(self):
        url = reverse('acivate_token', args=[self.uid, 'invalid Token 9999999'])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




