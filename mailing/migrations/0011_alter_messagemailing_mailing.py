# Generated by Django 4.2.9 on 2024-01-20 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0010_alter_mailing_сlient_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemailing',
            name='mailing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='Рассылки'),
            preserve_default=False,
        ),
    ]
