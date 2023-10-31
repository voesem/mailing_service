from django.conf import settings
from django.core.mail import send_mail
from mailing.models import Mailing, Log
from datetime import datetime, timedelta


def send_mailings(mailing):
    status_list = []
    mail_list = mailing.client.all()
    mailing.status = 'started'
    mailing.save()
    for client in mail_list:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
            )
        except Exception as e:
            response = {'attempt_status': Log.FAILED,
                        'response': 'Ошибка при отправке: {}'.format(str(e)),
                        'mailing': Mailing.objects.get(pk=mailing.id)}
            status_list.append(Log(**response))
        else:
            response = {'attempt_status': Log.SENT,
                        'response': 'Сообщение отправлено',
                        'mailing': Mailing.objects.get(pk=mailing.id)}
            status_list.append(Log(**response))
    Log.objects.bulk_create(status_list)


def start_mailing():
    mailings = Mailing.objects.all()
    print(mailings)
    for mailing in mailings:
        if mailing.mailing_status == Mailing.CREATED:
            obj = Log.objects.filter(mailing=mailing).last()

            if obj is None:
                mail_time = mailing.mailing_duration.replace(second=0, microsecond=0)
                now_time = datetime.now().time().replace(second=0, microsecond=0)
                if mail_time == now_time:
                    send_mailings(mailing)

            else:
                periodicity = mailing.frequency
                obj_time = obj.attempt_date_time

                if periodicity == Mailing.EVERY_DAY:
                    obj_time += timedelta(days=1)
                elif periodicity == Mailing.EVERY_WEEK:
                    obj_time += timedelta(days=7)
                elif periodicity == Mailing.EVERY_MONTH:
                    obj_time += timedelta(days=30)
                obj_time = obj_time.replace(second=0, microsecond=0)
                now_time = datetime.now().replace(second=0, microsecond=0)
                if obj_time == now_time:
                    send_mailings(mailing)
