from django.db import models

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


class Client(models.Model):
    email = models.EmailField(verbose_name='Контактный email')
    full_name = models.TextField(verbose_name='ФИО')
    comment = models.CharField(max_length=150, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.email} - {self.full_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    time_mailing = models.TimeField(verbose_name='Время рассылки')
    end_datatime_mailing = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время окончания рассылки')
    frequency = models.CharField(choices=FREQUENCY_CHOICES, default='1',
                                 verbose_name='Периодичность: раз в день, раз в неделю, раз в месяц')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Создана', verbose_name='Статус рассылки')

    def __str__(self):
        return f'{self.status} - {self.time_mailing}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MessageMailing(models.Model):
    topic = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылки', blank=True, null=True, )

    def __str__(self):
        return f'Тема:{self.topic} - {self.body}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщение для рассылок'


class LogsMailing(models.Model):
    date = models.DateTimeField(verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=100, verbose_name='Статус попытки')
    mail_response = models.TextField(max_length=100, verbose_name='Ответ почтового сервера')

    def __str__(self):
        return f'Тема:{self.status} - {self.date}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
