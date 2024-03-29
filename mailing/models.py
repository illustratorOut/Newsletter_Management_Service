import colorama
from django.conf import settings
from django.db import models, connection
from django.views import generic

NULLABLE = {'null': True, 'blank': True}

STATUS_CHOICES = (
    ('Завершена', 'Завершена'),
    ('Создана', 'Создана'),
    ('Запущена', 'Запущена'),
)

FREQUENCY_CHOICES = (
    ('1', 'раз в день'),
    ('7', 'раз в неделю'),
    ('30', 'раз в месяц'),
)


class Truncate:
    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            name_table = f'{cls.__module__.split(".")[0]}_{cls.__name__.lower()}'
            cursor.execute(f'TRUNCATE TABLE "{name_table}" RESTART IDENTITY CASCADE')
            print(colorama.Fore.GREEN + f'Таблица "{name_table}" очищена!' \
                  + colorama.Fore.RESET)


class Client(models.Model, Truncate):
    email = models.EmailField(verbose_name='Контактный email')
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.email} - {self.full_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model, Truncate):
    time_mailing = models.TimeField(verbose_name='Время рассылки')
    end_datatime_mailing = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    frequency = models.CharField(choices=FREQUENCY_CHOICES, default='1',
                                 verbose_name='Периодичность: раз в день, раз в неделю, раз в месяц')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Создана', verbose_name='Статус рассылки')
    сlient_key = models.ManyToManyField(Client, verbose_name='Пользователь', related_name='client')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return (
            f'{colorama.Fore.LIGHTYELLOW_EX + self.status + colorama.Fore.RESET} - '
            f'{colorama.Fore.GREEN + self.end_datatime_mailing.strftime("%d-%m-%Y %H:%M") + colorama.Fore.RESET} / '
            f'{colorama.Fore.MAGENTA + self.time_mailing.strftime("%H:%M") + colorama.Fore.RESET}')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-status', 'end_datatime_mailing']
        permissions = [
            (
                'set_status',
                'Can publish mailing'
            )
        ]


class MessageMailing(models.Model, Truncate):
    topic = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылки')

    def __str__(self):
        return f'Тема: {self.topic} - Сообщение: {self.body}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщение для рассылок'


class LogsMailing(models.Model, Truncate):
    date = models.DateTimeField(verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=100, verbose_name='Статус попытки')
    mail_response = models.TextField(max_length=100, verbose_name='Ответ почтового сервера')

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f'Тема:{self.status} - {self.date}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
