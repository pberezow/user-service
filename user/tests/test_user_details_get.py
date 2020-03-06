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


class TestUserDetailsGet(TestCase):
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
        non_admin_user_data = {
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
        another_licence_user_data = {
            'username': 'admin2',
            'password': 'admin123',
            'email': 'test3@test.pl',
            'licence_id': 1,
            'is_admin': True,
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'address': '',
            'position': ''
        }
        User.objects.create_user(**admin_user_data)
        User.objects.create_user(**non_admin_user_data)
        User.objects.create_user(**another_licence_user_data)

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

    def test_details_on_admin_self_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.get(
            reverse('user-details', kwargs={'user_id': 1})
        )

        self.assertEquals(response.status_code, status.HTTP_302_FOUND)
        self.assertEquals(response.data['licence_id'], 0)
        self.assertEquals(response.data['username'], 'admin')

    def test_details_on_admin_another_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.get(
            reverse('user-details', kwargs={'user_id': 2})
        )

        self.assertEquals(response.status_code, status.HTTP_302_FOUND)
        self.assertEquals(response.data['licence_id'], 0)
        self.assertEquals(response.data['username'], 'nonadmin')

    def test_details_on_admin_other_licence_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.get(
            reverse('user-details', kwargs={'user_id': 3})
        )

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_details_on_non_admin_self_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.non_admin_header)
        response = client.get(
            reverse('user-details', kwargs={'user_id': 2})
        )

        self.assertEquals(response.status_code, status.HTTP_302_FOUND)
        self.assertEquals(response.data['licence_id'], 0)
        self.assertEquals(response.data['username'], 'nonadmin')

    def test_details_on_non_admin_another_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.non_admin_header)
        response = client.get(
            reverse('user-details', kwargs={'user_id': 0})
        )

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
