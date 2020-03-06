import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from user.models import User
from group.models import Group
from django.core.management import call_command
from django.core.management.commands import flush
from user.serializers import UserDetailsSerializer

# initialize the APIClient app
client = APIClient()


class TestUserPermissions(TestCase):
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

        group_1 = {
            'name': 'Group1',
            'licence_id': 0
        }

        group_2 = {
            'name': 'Group2',
            'licence_id': 0
        }

        group_another_licence = {
            'name': 'Group3',
            'licence_id': 1
        }

        Group.objects.create(**group_1)
        Group.objects.create(**group_2)
        Group.objects.create(**group_another_licence)

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

    def test_set_permissions_on_admin_self_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.put(
            reverse('user-permissions', kwargs={'user_id': 1}),
            data=json.dumps({'groups': [
                {'name': 'Group1'}
            ]}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('groups', [{}])[0].get('name', None), 'Group1')

        modified_user = User.objects.get(pk=1)
        self.assertEquals(modified_user.groups.count(), 1)
        self.assertEquals(modified_user.groups.get().name, 'Group1')

    def test_set_permissions_on_admin_self_2groups_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.put(
            reverse('user-permissions', kwargs={'user_id': 1}),
            data=json.dumps({'groups': [
                {'name': 'Group1'},
                {'name': 'Group2'}
            ]}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data.get('groups', [])), 2)
        for group in response.data['groups']:
            name = group['name']
            self.assertEquals(name == 'Group1' or name == 'Group2', True)

        modified_user = User.objects.get(pk=1)
        self.assertEquals(modified_user.groups.count(), 2)
        for group in modified_user.groups.all():
            self.assertEquals(group.name == 'Group1' or group.name == 'Group2', True)

    def test_set_permissions_on_admin_self_another_licence_group_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.put(
            reverse('user-permissions', kwargs={'user_id': 1}),
            data=json.dumps({'groups': [
                {'name': 'Group3'}
            ]}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        modified_user = User.objects.get(pk=1)
        self.assertEquals(modified_user.groups.count(), 0)

    def test_set_permissions_on_admin_self_valid_and_another_licence_group_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.put(
            reverse('user-permissions', kwargs={'user_id': 1}),
            data=json.dumps({'groups': [
                {'name': 'Group1'},
                {'name': 'Group3'}
            ]}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        modified_user = User.objects.get(pk=1)
        self.assertEquals(modified_user.groups.count(), 0)

    def test_set_permissions_on_admin_another_user_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.put(
            reverse('user-permissions', kwargs={'user_id': 2}),
            data=json.dumps({'groups': [
                {'name': 'Group1'}
            ]}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('groups', [{}])[0].get('name', None), 'Group1')

        modified_user = User.objects.get(pk=2)
        self.assertEquals(modified_user.groups.count(), 1)
        self.assertEquals(modified_user.groups.get().name, 'Group1')

    def test_set_permissions_on_admin_another_licence_user_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.put(
            reverse('user-permissions', kwargs={'user_id': 3}),
            data=json.dumps({'groups': [
                {'name': 'Group1'}
            ]}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

        modified_user = User.objects.get(pk=3)
        self.assertEquals(modified_user.groups.count(), 0)

    def test_set_permissions_on_admin_another_licence_user_2_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.put(
            reverse('user-permissions', kwargs={'user_id': 3}),
            data=json.dumps({'groups': [
                {'name': 'Group3'}
            ]}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

        modified_user = User.objects.get(pk=3)
        self.assertEquals(modified_user.groups.count(), 0)
