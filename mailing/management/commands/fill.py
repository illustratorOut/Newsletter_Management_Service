from django.core.management import BaseCommand
from datetime import datetime, timedelta

from mailing.models import Client, Mailing, MessageMailing
from users.models import User
from random import choice


class Command(BaseCommand):
    def handle(self, *args, **options):
        Client.truncate()
        Mailing.truncate()
        MessageMailing.truncate()

        if User.objects.filter(email='bmgula55@mail.ru'):
            user = User.objects.filter(email='bmgula55@mail.ru')[0]
        else:
            user = User.objects.create(
                email='bmgula55@mail.ru',
                first_name='Admin',
                last_name='Adminov',
                # is_superuser=True,
                # is_staff=True,
                is_active=True,
                password='1234S5678'
            )
            password = '1234S5678'
            user.set_password(password)
            user.save()

        date = datetime.today()
        mailing_list = [
            # Дата <  Время >
            {'time_mailing': f'{(datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date - timedelta(1)}',
             'frequency': 1, 'status': 'Создана', 'owner': user},

            # 7
            {'time_mailing': f'{(datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date + timedelta(1)}',
             'frequency': 7, 'status': 'Создана', 'owner': user},
            # 30
            {'time_mailing': f'{(datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date - timedelta(1)}',
             'frequency': 30, 'status': 'Создана', 'owner': user},

            # Дата =  Время <
            {'time_mailing': f'{(datetime.now() - timedelta(hours=1)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date - timedelta(1)}',
             'frequency': 1, 'status': 'Создана', 'owner': user},
            # 7
            {'time_mailing': f'{(datetime.now() - timedelta(hours=1)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date - timedelta(1)}',
             'frequency': 7, 'status': 'Создана', 'owner': user},
            # 30
            {'time_mailing': f'{(datetime.now() - timedelta(hours=1)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date - timedelta(1)}',
             'frequency': 30, 'status': 'Создана', 'owner': user},

            # Дата =  Время >
            {'time_mailing': f'{(datetime.now() + timedelta(hours=2)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date}',
             'frequency': 1, 'status': 'Создана', 'owner': user},
            # 7
            {'time_mailing': f'{(datetime.now() + timedelta(hours=2)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date}',
             'frequency': 7, 'status': 'Создана', 'owner': user},
            # 30
            {'time_mailing': f'{(datetime.now() + timedelta(hours=2)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date}',
             'frequency': 30, 'status': 'Создана', 'owner': user},

            # Дата =  Время <
            {'time_mailing': f'{(datetime.now() - timedelta(hours=2)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date}',
             'frequency': 1, 'status': 'Создана', 'owner': user},
            # 7
            {'time_mailing': f'{(datetime.now() - timedelta(hours=2)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date}',
             'frequency': 7, 'status': 'Создана', 'owner': user},
            # 30
            {'time_mailing': f'{(datetime.now() - timedelta(hours=2)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date}',
             'frequency': 30, 'status': 'Создана', 'owner': user},

            # Дата >  Время >
            {'time_mailing': f'{(datetime.now() + timedelta(hours=3)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date + timedelta(1)}',
             'frequency': 1, 'status': 'Создана', 'owner': user},
            # 7
            {'time_mailing': f'{(datetime.now() + timedelta(hours=3)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date + timedelta(1)}',
             'frequency': 7, 'status': 'Создана', 'owner': user},
            # 30
            {'time_mailing': f'{(datetime.now() + timedelta(hours=3)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date + timedelta(1)}',
             'frequency': 30, 'status': 'Создана', 'owner': user},

            # Дата >  Время <
            {'time_mailing': f'{(datetime.now() - timedelta(hours=3)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date + timedelta(1)}',
             'frequency': 1, 'status': 'Создана', 'owner': user},
            # 7
            {'time_mailing': f'{(datetime.now() - timedelta(hours=3)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date + timedelta(1)}',
             'frequency': 7, 'status': 'Создана', 'owner': user},
            # 30
            {'time_mailing': f'{(datetime.now() - timedelta(hours=3)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date + timedelta(1)}',
             'frequency': 30, 'status': 'Создана', 'owner': user},
        ]
        Mailing.objects.bulk_create([Mailing(**mailing_item) for mailing_item in mailing_list])

        client = [Client.objects.create(email='bmgula55@mail.ru', full_name=f'Александр{i}') for i in
                  range(1, len(mailing_list) + 1)]

        for item in range(1, len(mailing_list) + 1):
            random_client = choice(client)
            my_post = Mailing.objects.get(pk=item)
            my_post.сlient_key.add(random_client)

        content = [{'topic': f'Сообщение{item}', 'body': f'Тело{item}', 'mailing': Mailing.objects.all()[item]} for item
                   in range(len(mailing_list))]
        MessageMailing.objects.bulk_create([MessageMailing(**content_item) for content_item in content])
