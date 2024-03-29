# Generated by Django 4.2.9 on 2024-01-21 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0011_alter_messagemailing_mailing'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='end_datatime_mailing',
            field=models.DateTimeField(verbose_name='Дата и время окончания рассылки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='сlient_key',
            field=models.ManyToManyField(related_name='client', to='mailing.client', verbose_name='Пользователь'),
        ),
    ]
