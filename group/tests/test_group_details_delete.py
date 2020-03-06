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


class TestGroupDetailsDelete(TestCase):
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
        User.objects.create_user(**admin_user_data)
        User.objects.create_user(**non_admin_user_data)

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

    def test_delete_group_on_admin(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.delete(
            reverse('group-details', kwargs={'group_name': 'Group1'})
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        group = Group.objects.filter(name='Group1')
        self.assertEquals(group.count(), 0)

    def test_delete_group_on_admin_another_licence_group(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_header)
        response = client.delete(
            reverse('group-details', kwargs={'group_name': 'Group3'})
        )

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

        group = Group.objects.filter(name='Group3')
        self.assertEquals(group.exists(), True)

    def test_delete_group_on_non_admin(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.non_admin_header)
        response = client.delete(
            reverse('group-details', kwargs={'group_name': 'Group1'})
        )

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        group = Group.objects.filter(name='Group1')
        self.assertEquals(group.exists(), True)
