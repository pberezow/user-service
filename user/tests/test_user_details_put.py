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


class TestUserDetailsPut(TestCase):
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
        response = client.put(
            reverse('user-details', kwargs={'user_id': 1}),
            data=json.dumps({'first_name': 'Admin', 'position': 'Position'}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['first_name'], 'Admin')
        self.assertEquals(response.data['position'], 'Position')

        modified_user = User.objects.get(pk=1)
        self.assertEquals(modified_user.first_name, 'Admin')
        self.assertEquals(modified_user.position, 'Position')

    def test_details_on_admin_another_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.put(
            reverse('user-details', kwargs={'user_id': 2}),
            data=json.dumps({'first_name': 'Nonadmin', 'position': 'Position'}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['first_name'], 'Nonadmin')
        self.assertEquals(response.data['position'], 'Position')

        modified_user = User.objects.get(pk=2)
        self.assertEquals(modified_user.first_name, 'Nonadmin')
        self.assertEquals(modified_user.position, 'Position')

    def test_details_on_non_admin_self_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.non_admin_header)
        response = client.put(
            reverse('user-details', kwargs={'user_id': 2}),
            data=json.dumps({'first_name': 'Admin', 'position': 'Position', 'phone_number': '012345678912'}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotEquals(response.data['first_name'], 'Admin')
        self.assertNotEquals(response.data['position'], 'Position')
        self.assertEquals(response.data['phone_number'], '012345678912')

        modified_user = User.objects.get(pk=2)
        self.assertNotEquals(modified_user.first_name, 'Admin')
        self.assertNotEquals(modified_user.position, 'Position')
        self.assertEquals(modified_user.phone_number, '012345678912')

    def test_details_on_non_admin_another_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.non_admin_header)
        response = client.put(
            reverse('user-details', kwargs={'user_id': 1}),
            data=json.dumps({'first_name': 'Admin', 'position': 'Position', 'phone_number': '012345678912'}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        modified_user = User.objects.get(pk=1)
        self.assertNotEquals(modified_user.first_name, 'Admin')
        self.assertNotEquals(modified_user.position, 'Position')
        self.assertNotEquals(modified_user.phone_number, '012345678912')

    def test_details_on_admin_another_licence_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.put(
            reverse('user-details', kwargs={'user_id': 3}),
            data=json.dumps({'first_name': 'Admin', 'position': 'Position', 'phone_number': '012345678912'}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

        modified_user = User.objects.get(pk=3)
        self.assertNotEquals(modified_user.first_name, 'Admin')
        self.assertNotEquals(modified_user.position, 'Position')
        self.assertNotEquals(modified_user.phone_number, '012345678912')
