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


class TestRegister(TestCase):
    def setUp(self):
        cmd = flush.Command()
        call_command(cmd, verbosity=0, interactive=False)
        admin_user_data = {
            'username': 'admin',
            'password': 'admin123',
            'email': 'test@test.pl',
            'licence_id': 0,
            'is_admin': True,
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'address': '',
            'position': ''
        }
        nonadmin_user_data = {
            'username': 'nonadmin',
            'password': 'nonadmin123',
            'email': 'test2@test.pl',
            'licence_id': 0,
            'is_admin': False,
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'address': '',
            'position': ''
        }
        User.objects.create_user(**admin_user_data)
        User.objects.create_user(**nonadmin_user_data)

        self.valid_user_payload = {
            'username': 'testuser',
            'password': 'test123test',
            'email': 'test@test.pl',
            'is_admin': False,
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'address': '',
            'position': ''
        }
        self.wrong_user_payload = {
            'password': 'test123test',
            'email': 'test1@test.pl',
            'is_admin': True,
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'address': '',
            'position': ''
        }
        self.empty_payload = {}

        response = client.post(
            reverse('user-login'),
            data=json.dumps({'username': 'admin', 'password': 'admin123'}),
            content_type='application/json'
        )
        self.admin_header = response.data['token']

        response = client.post(
            reverse('user-login'),
            data=json.dumps({'username': 'nonadmin', 'password': 'nonadmin123'}),
            content_type='application/json'
        )
        self.non_admin_header = response.data['token']

    def test_register_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.post(
            reverse('user-register'),
            data=json.dumps(self.valid_user_payload),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEquals(response.data['licence_id'], 0)

    def test_register_same_user_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.post(
            reverse('user-register'),
            data=json.dumps(self.valid_user_payload),
            content_type='application/json'
        )
        response = client.post(
            reverse('user-register'),
            data=json.dumps(self.valid_user_payload),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_by_non_admin_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.non_admin_header)
        response = client.post(
            reverse('user-register'),
            data=json.dumps(self.valid_user_payload),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_wrong_payload(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.post(
            reverse('user-register'),
            data=json.dumps(self.wrong_user_payload),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
