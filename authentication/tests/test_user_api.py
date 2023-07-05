from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from user.models import User

from rest_framework.test import APIClient
from rest_framework import status

class PublicUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "username": 'Nimaa',
            "email": 'nima.nilchian2@gmail.com',
            'password': '123456',
            'password2': '123456'
        }

    def test_create_valid_user(self):
        """Test Creating user with valid payload"""
        signup_url = reverse('register')

        response = self.client.post(signup_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=response.data['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exist(self):
        """Test if user exist"""
        signup_url = reverse('register')

        baker.make(User, email=self.payload['email'], username=self.payload['username'])
        response = self.client.post(signup_url, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_successfully(self):
        """Test login successfully with right payload"""
        url = reverse('login')
        payload = {
            "username": 'Nimaa',
            "email": 'nima.nilchian3@gmail.com',
            "password": "123456"
        }

        get_user_model().objects.create_user(**payload)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


    def test_login_without_register(self):
        url = reverse('login')
        payload = {
            "email": 'nima.nilchian3@gmail.com',
            "password": "123456"
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


class PrivateUserAPITest(TestCase):
    def setUp(self):
        self.payload = {
            "email": 'nima.nilchian2@gmail.com',
            'password': '123456',
        }
        self.user = get_user_model().objects.create_user(**self.payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_verify_email_successfully(self):
        response = self.client.post(reverse('login'), self.payload)
        token = response.data['token']
        self.assertTrue(token)

        response = self.client.get(reverse('email-verify'), {'token': token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        """Test change password with correct payload"""
        payload = {
            'old_password': '123456',
            'new_password': '123'
        }
        response = self.client.put(reverse('change-password'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_wrong(self):
        """Test change password with wrong credentials"""
        payload = {
            'old_password': '12345',
            'new_password': '123'
        }
        response = self.client.put(reverse('change-password'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(reverse('change-password'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password(self):
        url = reverse('request-password-reset')

        """Test if reset password successful with right email"""
        response = self.client.post(url, {'email': 'nima.nilchian2@gmail.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Test if reset password fail with wrong email"""
        response = self.client.post(url, {'email': 'nima.nilchi@gmail.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
