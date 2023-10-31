from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name='контактный email', unique=True)
    name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='cоздатель', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='cоздатель', **NULLABLE)

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    EVERY_DAY = 'every_day'
    EVERY_WEEK = 'every_week'
    EVERY_MONTH = 'every_month'

    FREQUENCY_TYPES = (
        (EVERY_DAY, 'раз в день'),
        (EVERY_WEEK, 'раз в неделю'),
        (EVERY_MONTH, 'раз в месяц'),
    )

    COMPLETED = 'completed'
    CREATED = 'created'
    LAUNCHED = 'launched'

    STATUS_TYPES = (
        (COMPLETED, 'завершена'),
        (CREATED, 'создана'),
        (LAUNCHED, 'запущена'),
    )

    mailing_duration = models.TimeField(verbose_name='время рассылки')
    frequency = models.CharField(max_length=11, choices=FREQUENCY_TYPES, verbose_name='периодичность')
    mailing_status = models.CharField(
        max_length=9, choices=STATUS_TYPES, default=CREATED, verbose_name='статус рассылки'
    )
    client = models.ManyToManyField(Client, verbose_name='клиент')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='cоздатель', **NULLABLE)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('id',)


class Log(models.Model):

    SENT = 'sent'
    FAILED = 'failed'
    PENDING = 'pending'

    STATUS_CHOICES = (
        (SENT, 'Отправлено'),
        (FAILED, 'Не удалось отправить'),
        (PENDING, 'В ожидании')
    )

    creation_time = models.TimeField(auto_now_add=True, verbose_name='дата создания', **NULLABLE)
    attempt_date_time = models.DateTimeField(
        auto_now_add=True, verbose_name='дата и время последней попытки', **NULLABLE
    )
    attempt_status = models.CharField(
        max_length=10, verbose_name='статус попытки', choices=STATUS_CHOICES, default=PENDING
    )
    response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка', **NULLABLE)

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылки'
