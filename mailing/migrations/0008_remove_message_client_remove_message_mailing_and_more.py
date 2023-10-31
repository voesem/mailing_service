# Generated by Django 4.2.6 on 2023-10-29 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0007_remove_mailing_client_message_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='client',
        ),
        migrations.RemoveField(
            model_name='message',
            name='mailing',
        ),
        migrations.AddField(
            model_name='mailing',
            name='client',
            field=models.ManyToManyField(to='mailing.client', verbose_name='клиент'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.log', verbose_name='сообщение'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='сообщение'),
        ),
    ]