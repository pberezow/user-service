from django.conf import settings
from django.core.management.base import BaseCommand
from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').count() == 0:
            print('Creating admin account with credentials: admin / admin123')
            data = {
                'username': 'admin',
                'password': 'admin123',
                'licence_id': 1,
                'email': 'wojtczitolamus@gmail.com',
                'is_admin': True
            }
            admin = User.objects.create_superuser(**data)
            # for user in settings.ADMINS:
            #     username = user[0].replace(' ', '')
            #     email = user[1]
            #     password = 'admin'
            #     print('Creating account for %s (%s)' % (username, email))
            #     admin = Account.objects.create_superuser(email=email, username=username, password=password)
            #     admin.is_active = True
            #     admin.is_admin = True
            #     admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')