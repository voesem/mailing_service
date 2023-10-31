# Generated by Django 4.2.6 on 2023-10-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_alter_mailing_mailing_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='message',
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ManyToManyField(to='mailing.message', verbose_name='сообщение'),
        ),
    ]