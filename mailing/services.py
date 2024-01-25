import datetime

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing, MessageMailing


def get_send_mail(mail, mail_header, mail_body):
    """Отправка рассылок на почту"""
    send_mail(
        subject=mail_header,
        message=mail_body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[mail],
    )
    return send_mail


def run_newsletter():
    '''Список рассылок'''

    print('Отправка рассылок')
    сurrent_time = datetime.datetime.today().strftime('%H:%M')
    # __gte - Больще или равно
    # __lte - Меньше или равно

    # newskatters = Mailing.objects.all().filter(status='Создана').filter(time_mailing__lte=сurrent_time).filter(
    #     end_datatime_mailing__gte=f'{datetime.datetime.today().strftime("%Y-%m-%d")}T{datetime.datetime.today().strftime("%H:%M")}')

    newskatters = Mailing.objects.all().filter(status='Создана')

    for i in newskatters:
        date_time_str = str(datetime.datetime.today())
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

        date_time_str2 = str(i.end_datatime_mailing.strftime('%Y-%m-%d %H:%M:%S.%f'))
        date_time_obj2 = datetime.datetime.strptime(date_time_str2, '%Y-%m-%d %H:%M:%S.%f')

        if date_time_obj2 >= date_time_obj:
            # Дата >= Текущая дата

            print(i)
            print(i.time_mailing)
            print(datetime.time())


            if i.time_mailing >= datetime.time():
                # Время >= Текущее время

                pass

            else:
                # Время <= Текущее время
                i.status = 'Запущена'
                i.save()

        else:
            # Дата <= Текущая дата
            print(newskatters)
            i.status = 'Завершена'
            i.save()

# if newskatters_b:
#     mailing = Mailing.objects.all().filter(status='Запущена')
#     # print(mailing)
#     for task in mailing:
#         for client in task.сlient_key.all():
#             message = MessageMailing.objects.filter(mailing=task)
#             for k in message:
#                 get_send_mail(client, k.topic, k.body)
#                 try:
#                     data = datetime.datetime.now() + datetime.timedelta(int(task.frequency))
#                     # Реализовать проверку если дата не больше отправки сообщения тогда переводить в статус Запущена
#                     print(task.end_datatime_mailing)
#                     print('-------------------')
#                     print(data)
#                     if task.end_datatime_mailing > data:
#                         task.status = 'Запущена'
#                         task.save()
#                     else:
#                         task.status = 'Завершена'
#                         task.save()
#                 except:
#                     # Реализовать логику - логирования статистики отправленных сообщений
#                     task.status = 'Завершена'
#                     task.save()

# # Дальше получаем список клиентов в конце проверяем следующую дату отпраавки, если дата отправки коeректна то меняем 'run' на 'created'
