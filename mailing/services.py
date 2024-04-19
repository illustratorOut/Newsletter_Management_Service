import smtplib
from datetime import datetime, timezone, timedelta

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing, MessageMailing, LogsMailing


def _send_mail(mail, header, body, mailing):
    """Отправка рассылок на почту плюс логирование"""
    date = datetime.now(timezone.utc)

    try:
        send_mail(
            subject=header,
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=mail,
            fail_silently=False,
        )
        log = LogsMailing.objects.create(date=date, mail_response=send_mail, status='Успешно', mailing=mailing)
    except smtplib.SMTPException as e:
        log = LogsMailing.objects.create(date=date, mail_response=e, status='Ошибка', mailing=mailing)
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
    handler_email1(launched_mailing, current_date_time, current_time)


def handler_email(сreated_mailing, current_date_time, current_time):
    for mailing in сreated_mailing:
        if current_date_time > mailing.end_datatime_mailing:
            ''' Если текущее дата и время больше >  даты и времени окончания рассылки '''
            client = [client.email for client in mailing.сlient_key.all()]
            message = MessageMailing.objects.filter(mailing=mailing.pk)
            sending_messages = [_send_mail(client, row.topic, row.body, mailing) for row in message]

            # <QuerySet [<MessageMailing: Тема: Сообщение4 - Сообщение: Тело4>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение0 - Сообщение: Тело0>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение1 - Сообщение: Тело1>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение2 - Сообщение: Тело2>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение3 - Сообщение: Тело3>]>

            mailing.status = 'Завершена'
            mailing.save()
            continue

        elif current_time >= mailing.time_mailing and current_date_time < mailing.end_datatime_mailing:
            ''' Если текущее время больше > времени начала и текущее дата и время меньше < даты и времени окончания '''

            print('______________запущена_отправка_для_всех_этих_клиентов______________')
            client = [client.email for client in mailing.сlient_key.all()]
            message = MessageMailing.objects.filter(mailing=mailing.pk)

            sending_messages = [_send_mail(client, row.topic, row.body, mailing) for row in message]

            # <QuerySet [<MessageMailing: Тема: Сообщение5 - Сообщение: Тело5>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение6 - Сообщение: Тело6>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение7 - Сообщение: Тело7>,
            # <MessageMailing: Тема: Сообщение8 - Сообщение: Тело8>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение9 - Сообщение: Тело9>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение10 - Сообщение: Тело10>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение11 - Сообщение: Тело11>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение12 - Сообщение: Тело12>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение13 - Сообщение: Тело13>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение14 - Сообщение: Тело14>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение15 - Сообщение: Тело15>]>
            # <QuerySet [<MessageMailing: Тема: Сообщение17 - Сообщение: Тело17>]>

            if mailing.end_datatime_mailing > timedelta(days=int(mailing.frequency)) + current_date_time:
                ''' Дата окончания рассылки больше > шаг(1,7,30 дней) + текущая дата  '''
                mailing.status = 'Запущена'
                mailing.save()
                # <QuerySet [<MessageMailing: Тема: Сообщение12 - Сообщение: Тело12>]>
                # <QuerySet [<MessageMailing: Тема: Сообщение15 - Сообщение: Тело15>]>


            else:
                mailing.status = 'Завершена'
                mailing.save()

        elif current_time <= mailing.time_mailing and current_date_time < mailing.end_datatime_mailing:
            ''' Если текущее время < меньше времени рассылки и текущая дата и время < даты и времени окончания'''
            mailing.status = 'Запущена'
            mailing.save()
            message = MessageMailing.objects.filter(mailing=mailing.pk)
            print(message)


def handler_email1(launched_mailing, current_date_time, current_time):
    for mailing in launched_mailing:
        if current_date_time > mailing.end_datatime_mailing:
            ''' Если текущее дата и время больше >  даты и времени окончания рассылки '''
            client = [client.email for client in mailing.сlient_key.all()]
            message = MessageMailing.objects.filter(mailing=mailing.pk)
            sending_messages = [_send_mail(client, row.topic, row.body, mailing) for row in message]

            mailing.status = 'Завершена'
            mailing.save()
            continue

        elif current_time >= mailing.time_mailing and current_date_time < mailing.end_datatime_mailing:
            ''' Если текущее время больше > времени начала и текущее дата и время меньше < даты и времени окончания '''

            if mailing.end_datatime_mailing > timedelta(days=int(mailing.frequency)) + current_date_time:
                ''' Дата окончания рассылки больше > шаг(1,7,30 дней) + текущая дата  '''
                mailing.status = 'Запущена'
                mailing.save()
            else:
                print('______________запущена_отправка_для_всех_этих_клиентов______________')
                client = [client.email for client in mailing.сlient_key.all()]
                message = MessageMailing.objects.filter(mailing=mailing.pk)
                sending_messages = [_send_mail(client, row.topic, row.body, mailing) for row in message]

                mailing.status = 'Завершена'
                mailing.save()

        elif current_time <= mailing.time_mailing and current_date_time < mailing.end_datatime_mailing:
            mailing.status = 'Запущена'
            mailing.save()
