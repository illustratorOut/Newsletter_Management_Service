# Generated by Django 4.2.9 on 2024-01-16 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_mailing_сlient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='сlient',
        ),
        migrations.AddField(
            model_name='mailing',
            name='сlient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mailing.client', verbose_name='Пользователь'),
            preserve_default=False,
        ),
    ]
