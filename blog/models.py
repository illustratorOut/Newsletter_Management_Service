from django.conf import settings
from django.db import models

from mailing.models import Truncate

NULLABLE = {
    'null': 'True',
    'blank': 'True',
}


class Blog(models.Model, Truncate):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.CharField(**NULLABLE, max_length=150, verbose_name='slug')
    body = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='Изображение')
    date_create = models.DateTimeField(**NULLABLE, auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    count_views = models.IntegerField(**NULLABLE, default=0, verbose_name='Количество просмотров')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.title} {self.date_create}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'

        permissions = [
            ('set_is_published', 'Может публиковать товары'),
        ]
