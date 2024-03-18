from datetime import datetime, timezone, timedelta

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing, MessageMailing, LogsMailing


def _send_mail(mail, header, body):
    """Отправка рассылок на почту"""
    send_mail(
        subject=header,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=mail,
        fail_silently=False,
    )
    return send_mail


def log_send_mail(respons_email, mailing):
    ''' Логирования: по ходу отправки сообщений собирается статистика '''
    date = datetime.now(timezone.utc)

    if respons_email:
        log = LogsMailing.objects.create(date=date, mail_response=respons_email, status='Успешно', mailing=mailing)
    else:
        log = LogsMailing.objects.create(date=date, mail_response=respons_email, status='Ошибка', mailing=mailing)
    log.save()


def run_newsletter():
    '''Список рассылок'''
    # __gte - Больще или равно
    # __lte - Меньше или равно

    сreated_mailing = Mailing.objects.all().filter(status='Создана')
    launched_mailing = Mailing.objects.all().filter(status='Запущена')
    current_date_time = datetime.now(timezone.utc)
    current_time = datetime.now().time()

    print(сreated_mailing)

    handler_email(сreated_mailing, current_date_time, current_time)
    handler_email(launched_mailing, current_date_time, current_time)


def handler_email(сreated_mailing, current_date_time, current_time):
    for mailing in сreated_mailing:
        if current_date_time > mailing.end_datatime_mailing:
            ''' Если текущее дата и время больше >  даты и времени окончания рассылки '''
            client = [client.email for client in mailing.сlient_key.all()]
            message = MessageMailing.objects.filter(mailing=mailing.pk)
            sending_messages = [_send_mail(client, row.topic, row.body) for row in message]
            log_send_mail(sending_messages, mailing)

            mailing.status = 'Завершена'
            mailing.save()
            continue

        elif current_time >= mailing.time_mailing and current_date_time < mailing.end_datatime_mailing:
            ''' Если текущее время больше > времени начала и текущее дата и время меньше < даты и времени окончания '''

            print('______________запущена_отправка_для_всех_этих_клиентов______________')
            client = [client.email for client in mailing.сlient_key.all()]
            message = MessageMailing.objects.filter(mailing=mailing.pk)
            sending_messages = [_send_mail(client, row.topic, row.body) for row in message]
            log_send_mail(sending_messages, mailing)

            if mailing.end_datatime_mailing > timedelta(days=int(mailing.frequency)) + current_date_time:
                ''' Дата окончания рассылки больше > шаг(1,7,30 дней) + текущая дата  '''
                mailing.status = 'Запущена'
                mailing.save()
            else:
                mailing.status = 'Завершена'
                mailing.save()

        elif current_time <= mailing.time_mailing and current_date_time < mailing.end_datatime_mailing:
            mailing.status = 'Запущена'
            mailing.save()
