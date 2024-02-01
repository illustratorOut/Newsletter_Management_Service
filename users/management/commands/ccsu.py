from django.core.management import BaseCommand

from mailing.services import log_print_crate_user
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='Adminov',
            is_superuser=True,
            is_staff=True,
            is_active=True,
            password='1234S5678'
        )
        password = '1234S5678'
        user.set_password(password)
        user.save()

        log_print_crate_user(user, password)

        user2 = User.objects.create(
            email='user@sky.pro',
            first_name='User',
            last_name='Users',
            is_active=True,
        )
        user2.set_password('1234S5678')
        user2.save()
