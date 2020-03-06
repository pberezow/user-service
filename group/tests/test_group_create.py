import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from user.models import User
from group.models import Group
from django.core.management import call_command
from django.core.management.commands import flush

# initialize the APIClient app
client = APIClient()


class TestGroupCreate(TestCase):
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

    def test_create_group_on_admin_success(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.post(
            reverse('group-list-create'),
            data=json.dumps({'name': 'Group1'}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data.get('name', None), 'Group1')
        self.assertEquals(response.data.get('licence_id', None), 0)

        group = Group.objects.filter(name='Group1')
        self.assertEquals(group.exists(), True)
        self.assertEquals(group.get().name, 'Group1')
        self.assertEquals(group.get().licence_id, 0)

    def test_create_group_on_admin_already_exists_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.post(
            reverse('group-list-create'),
            data=json.dumps({'name': 'Group1'}),
            content_type='application/json'
        )

        response = client.post(
            reverse('group-list-create'),
            data=json.dumps({'name': 'Group1'}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        group = Group.objects.filter(name='Group1')
        self.assertEquals(group.count(), 1)
        self.assertEquals(group.get().name, 'Group1')
        self.assertEquals(group.get().licence_id, 0)

    def test_create_group_on_admin_wrong_payload_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.post(
            reverse('group-list-create'),
            data=json.dumps({'name__': 'Group1'}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        group = Group.objects.filter(name='Group1')
        self.assertEquals(group.exists(), False)

    def test_create_group_on_admin_no_payload(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.post(
            reverse('group-list-create'),
            data=json.dumps(None),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        group = Group.objects.all()
        self.assertEquals(group.exists(), False)

    def test_create_group_on_admin_with_licence_id(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.post(
            reverse('group-list-create'),
            data=json.dumps({'name': 'Group1', 'licence_id': 10}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data.get('name', None), 'Group1')
        self.assertEquals(response.data.get('licence_id', None), 0)

        group = Group.objects.filter(name='Group1')
        self.assertEquals(group.exists(), True)
        self.assertEquals(group.get().name, 'Group1')
        self.assertEquals(group.get().licence_id, 0)

    def test_create_group_on_non_admin_failed(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.non_admin_header)
        response = client.post(
            reverse('group-list-create'),
            data=json.dumps({'name': 'Group1'}),
            content_type='application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        group = Group.objects.filter(name='Group1')
        self.assertEquals(group.exists(), False)
