# Generated by Django 4.2.6 on 2023-10-29 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0009_alter_mailing_log_alter_mailing_mailing_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'ordering': ('id',), 'verbose_name': 'рассылка', 'verbose_name_plural': 'рассылки'},
        ),
    ]
