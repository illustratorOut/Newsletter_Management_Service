from colorama import Fore
from colorama import Fore
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from mailing.models import Mailing
from users.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):

    def handle(self, *args, **options):
        dict_user = {
            'user_admin': {
                'email': 'admin@sky.pro',
                'first_name': 'Admin',
                'last_name': 'Adminov',
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
                'password': '1234S5678'},

            'user_moder': {
                'email': 'manager@sky.pro',
                'first_name': 'Manager',
                'last_name': 'Managers',
                'is_active': True,
                'password': '1234S5678'},

            'user_uses': {
                'email': 'user@sky.pro',
                'first_name': 'User',
                'last_name': 'Users',
                'is_active': True,
                'password': '1234S5678'},
        }

        for row in dict_user:
            email = dict_user[row]['email']
            password = dict_user[row]['password']

            if User.objects.filter(email=email):
                print(
                    f'Пользователь' + Fore.RED + f' {email} ' + Fore.RESET + f'уже существует! password: ({Fore.GREEN}{password}{Fore.RESET})')
            else:
                user = User.objects.create(**dict_user[row])
                user.set_password(password)
                user.save()
                print(
                    f'{Fore.GREEN}Пользователь создан!\n {Fore.RESET}login: {Fore.GREEN} {user.email}\n {Fore.RESET}password: {Fore.GREEN}{password}{Fore.RESET}\n')

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_group('Менеджер')
        self.add_permissions('Менеджер')

        user = User.objects.get(email='manager@sky.pro')
        my_group = Group.objects.get(name='Менеджер')
        my_group.user_set.add(user)

    def add_group(self, name_group):
        ''' Создаем Groups() Пример:Менеджер '''
        manager_group = Group.objects.get_or_create(name=name_group)
        print(f'Группа' + Fore.GREEN + f' "{name_group}" ' + Fore.RESET + 'созданна!')
        return manager_group

    def add_permissions(self, name_group: str):
        manager_group = Group.objects.filter(name=name_group).get()
        print(f'Группе' + Fore.GREEN + f' "{name_group}" ' + Fore.RESET + 'добавленны права:')

        ct = ContentType.objects.get_for_model(User)
        post_permission = Permission.objects.filter(content_type=ct)
        for perm in post_permission:
            if perm.codename == "view_user":
                manager_group.permissions.add(perm)
                print('+ ' + Fore.GREEN + f'{perm}' + Fore.RESET)

        ct = ContentType.objects.get_for_model(Mailing)
        post_permission = Permission.objects.filter(content_type=ct)
        for perm in post_permission:
            if perm.codename in ["view_mailing", "change_mailing"]:
                manager_group.permissions.add(perm)
                print('+ ' + Fore.GREEN + f'{perm}' + Fore.RESET)

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
