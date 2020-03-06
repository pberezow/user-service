import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from user.models import User
from django.core.management import call_command
from django.core.management.commands import flush
from user.serializers import UserDetailsSerializer

# initialize the APIClient app
client = APIClient()


class TestLogout(TestCase):
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
        User.objects.create_user(**admin_user_data)

        response = client.post(
            reverse('user-login'),
            data=json.dumps({'username': 'admin', 'password': 'admin123'}),
            content_type='application/json'
        )
        self.admin_header = response.data['token']

    def test_logout_success(self):
        self.assertNotEquals(client.cookies['token'].value, '')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.get(
            reverse('user-logout')
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(client.cookies['token'].value, '')

    def test_logout_unauthorized(self):
        self.assertNotEquals(client.cookies['token'].value, '')
        client.credentials()
        response = client.get(
            reverse('user-logout')
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEquals(client.cookies['token'].value, '')
