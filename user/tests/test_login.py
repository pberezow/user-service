import json
from rest_framework import status
from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from user.models import User
from django.core.management import call_command
from django.core.management.commands import flush
from user.serializers import UserDetailsSerializer

# initialize the APIClient app
client = APIClient()


class TestLogin(TestCase):
    def setUp(self):
        cmd = flush.Command()
        call_command(cmd, verbosity=0, interactive=False)
        user_data = {
            'username': 'testuser',
            'password': 'test123test',
            'email': 'test@test.pl',
            'is_admin': True,
            'licence_id': 0,
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'address': '',
            'position': ''
        }
        User.objects.create_user(**user_data)
        self.valid_payload = {
            'username': 'testuser',
            'password': 'test123test'
        }
        self.wrong_password_payload = {
            'username': 'testuser',
            'password': 'test123testwrong'
        }
        self.empty_payload = {}

    def test_login_success(self):
        response = client.post(
            reverse('user-login'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('token', response.cookies)

    def test_login_failed(self):
        response = client.post(
            reverse('user-login'),
            data=json.dumps(self.wrong_password_payload),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', response.data)
        self.assertNotIn('token', response.cookies)

    def test_login_empty_body(self):
        response = client.post(
            reverse('user-login'),
            data=json.dumps(self.empty_payload),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', response.data)
        self.assertNotIn('token', response.cookies)
