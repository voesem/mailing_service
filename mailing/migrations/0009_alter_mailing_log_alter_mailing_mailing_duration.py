# Generated by Django 4.2.6 on 2023-10-29 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0008_remove_message_client_remove_message_mailing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.log', verbose_name='лог'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='mailing_duration',
            field=models.TimeField(verbose_name='время рассылки'),
        ),
    ]
