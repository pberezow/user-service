from django.conf import settings
from django.core.management.base import BaseCommand
from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in settings.ADMINS:

            try:
                if User.objects.filter(username=user[0]).count() == 0:
                    print(f'Creating admin account with credentials: {user[0]} / {user[1]}')
                    data = {
                        'username': user[0],
                        'password': user[1],
                        'licence_id': 1,
                        'email': user[2],
                        'is_admin': True
                    }
                    admin = User.objects.create_superuser(**data)

                else:
                    print(f'Admin {user[0]} already exists.')

            except IndexError as e:
                print('Cannot create user - IndexError (See settings.ADMINS)')
