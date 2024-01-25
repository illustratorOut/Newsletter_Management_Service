from django.core.management import BaseCommand
from datetime import datetime, timedelta

from mailing.models import Client, Mailing, MessageMailing
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        Client.truncate()
        Mailing.truncate()
        MessageMailing.truncate()
        if User.objects.filter(email='bmgula55@mail.ru'):
            user = User.objects.filter(email='bmgula55@mail.ru')
        else:
            user = User.objects.create(email='bmgula55@mail.ru', is_active=True)

        date = datetime.today()

        mailing_list = [
            # Дата <  Время >
            {'time_mailing': f'{(datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date - timedelta(1)}',
             'frequency': 1, 'status': 'Создана', 'owner': user[0]},

            # Дата =  Время <
            {'time_mailing': f'{(datetime.now() - timedelta(hours=1)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date - timedelta(1)}',
             'frequency': 1, 'status': 'Создана', 'owner': user[0]},

            # Дата =  Время >
            {'time_mailing': f'{(datetime.now() + timedelta(hours=2)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date}',
             'frequency': 1, 'status': 'Создана', 'owner': user[0]},

            # Дата =  Время <
            {'time_mailing': f'{(datetime.now() - timedelta(hours=2)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date}',
             'frequency': 1, 'status': 'Создана', 'owner': user[0]},

            # Дата >  Время >
            {'time_mailing': f'{(datetime.now() + timedelta(hours=3)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date + timedelta(1)}',
             'frequency': 1, 'status': 'Создана', 'owner': user[0]},

            # Дата >  Время <
            {'time_mailing': f'{(datetime.now() - timedelta(hours=3)).strftime("%H:%M:%S")}',
             'end_datatime_mailing': f'{date + timedelta(1)}',
             'frequency': 1, 'status': 'Создана', 'owner': user[0]},
        ]
        Mailing.objects.bulk_create([Mailing(**mailing_item) for mailing_item in mailing_list])

        my_client1 = Client.objects.create(email='bmgula55@mail.ru', full_name='Александр1')
        my_client2 = Client.objects.create(email='bmgula55@mail.ru', full_name='Александр2')
        my_client3 = Client.objects.create(email='bmgula55@mail.ru', full_name='Александр3')
        my_client4 = Client.objects.create(email='bmgula55@mail.ru', full_name='Александр4')
        my_client5 = Client.objects.create(email='bmgula55@mail.ru', full_name='Александр5')
        my_client6 = Client.objects.create(email='bmgula55@mail.ru', full_name='Александр6')

        my_post1 = Mailing.objects.get(pk=1)
        my_post2 = Mailing.objects.get(pk=2)
        my_post3 = Mailing.objects.get(pk=3)
        my_post4 = Mailing.objects.get(pk=4)
        my_post5 = Mailing.objects.get(pk=5)
        my_post6 = Mailing.objects.get(pk=6)

        my_post1.сlient_key.add(my_client1)
        my_post2.сlient_key.add(my_client2)
        my_post3.сlient_key.add(my_client3)
        my_post4.сlient_key.add(my_client4)
        my_post5.сlient_key.add(my_client5)
        my_post6.сlient_key.add(my_client6)

        message_content = Mailing.objects.all()
        content_list = [
            {'topic': 'Сообщение1', 'body': 'Тело1', 'mailing': message_content[0]},
            {'topic': 'Сообщение2', 'body': 'Тело2', 'mailing': message_content[1]},
            {'topic': 'Сообщение3', 'body': 'Тело3', 'mailing': message_content[2]},
            {'topic': 'Сообщение4', 'body': 'Тело4', 'mailing': message_content[3]},

        ]
        MessageMailing.objects.bulk_create([MessageMailing(**content_item) for content_item in content_list])
