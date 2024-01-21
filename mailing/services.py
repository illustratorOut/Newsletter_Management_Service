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

    newskatters = Mailing.objects.all().filter(status='Создана').filter(time_mailing__lte=сurrent_time).filter(
        end_datatime_mailing__gte=f'{datetime.datetime.today().strftime("%Y-%m-%d")}T{datetime.datetime.today().strftime("%H:%M")}')

    newskatters_ = Mailing.objects.all().filter(status='Создана').filter(time_mailing__gte=сurrent_time)

    print(newskatters_)

    if newskatters:
        #  меньше или равно  - текущее время 23:18
        print(f'меньше или равно {сurrent_time}')
        pass

    if newskatters_:
        # + учитывать интервалл рассылок:
        print(f'Больше или равно {сurrent_time}')

        for newskatter_ in newskatters_:
            newskatter_.status = 'Запущена'
            newskatter_.save()

    for newskatter in newskatters:
        newskatter.status = 'Запущена'
        newskatter.save()

    mailing = Mailing.objects.all().filter(status='Запущена')

    # Есть информация о клиентах которые привязаны к рассылке
    for task in mailing:
        # print(task.сlient_key.all())
        for client in task.сlient_key.all():
            # print(client)
            message = MessageMailing.objects.filter(mailing=task)
            for k in message:
                try:
                    email_results = get_send_mail(client, k.topic, k.body)

                    data = datetime.datetime.now() + datetime.timedelta(int(task.frequency))
                    # Реализовать проверку если дата не больше отправки сообщения тогда переводить в статус Запущена
                    print(task.end_datatime_mailing)
                    print('-------------------')
                    print(data)
                    if task.end_datatime_mailing > data:
                        task.status = 'Запущена'
                        task.save()
                    else:
                        task.status = 'Завершена'
                        task.save()
                except:
                    # Реализовать логику - логирования статистики отправленных сообщений
                    task.status = 'Завершена'
                    task.save()

    # # Дальше получаем список клиентов в конце проверяем следующую дату отпраавки, если дата отправки коректна то меняем 'run' на 'created'
