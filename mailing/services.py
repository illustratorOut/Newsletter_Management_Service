import datetime

import colorama
from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing, MessageMailing, LogsMailing


def log_print_crate_user(user, password):
    print(
        colorama.Fore.GREEN + f'Пользователь создан!\n' + colorama.Fore.RESET + 'login: ' + colorama.Fore.GREEN + f'{user.email}\n' + colorama.Fore.RESET + 'password: ' + colorama.Fore.GREEN + f'{password}' + colorama.Fore.RESET)


def get_send_mail(mail, mail_header, mail_body):
    """Отправка рассылок на почту"""

    send_mail(
        subject=mail_header,
        message=mail_body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[mail],
        # fail_silently=False,
    )
    return send_mail


def run_newsletter():
    '''Список рассылок'''

    print('Отправка рассылок')
    # __gte - Больще или равно
    # __lte - Меньше или равно

    #     end_datatime_mailing__gte=f'{datetime.datetime.today().strftime("%Y-%m-%d")}T{datetime.datetime.today().strftime("%H:%M")}')

    newskatters = Mailing.objects.all().filter(status='Создана')

    for i in newskatters:
        date_time_str = str(datetime.datetime.today())
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

        date_time_str2 = str(i.end_datatime_mailing.strftime('%Y-%m-%d %H:%M:%S.%f'))
        date_time_obj2 = datetime.datetime.strptime(date_time_str2, '%Y-%m-%d %H:%M:%S.%f')

        if date_time_obj2 >= date_time_obj:
            # Дата >= Текущая дата

            if i.time_mailing >= datetime.datetime.now().time():
                # Время >= Текущее время
                pass
            else:
                # Время <= Текущее время
                i.status = 'Запущена'
                i.save()

                for client in i.сlient_key.all():
                    message = MessageMailing.objects.filter(mailing=i.pk)
                    for k in message:
                        response_email = get_send_mail(client.email, k.topic, k.body)

                        print(response_email)
                log = LogsMailing.objects.create(
                    date=datetime.datetime.today(),
                    status=True,
                    mail_response=str(response_email),
                    mailing=i,
                )
                log.save()

                print(i.time_mailing)
                print(i.end_datatime_mailing.time())
                if i.time_mailing >= i.end_datatime_mailing.time():
                    # Время <= Текущее время
                    i.status = 'Завершено'
                    i.save()


        else:
            # Дата <= Текущая дата
            i.status = 'Завершена'
            i.save()

# # Дальше получаем список клиентов в конце проверяем следующую дату отпраавки, если дата отправки коeректна то меняем 'run' на 'created'
