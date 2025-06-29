from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingAttempt


def send_mailing(mailing):
    recipients = mailing.recipients.all()
    successful_attempts = 0
    total_recipients = recipients.count()

    for recipient in recipients:
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.body,
                EMAIL_HOST_USER,
                [recipient.email],
            )
            MailingAttempt.objects.create(
                date_attempt=timezone.now(),
                status="SU",
                mail_response="Сообщение отправлено",
                mailing=mailing,
            )
            successful_attempts += 1
            print(
                f"Сообщение {mailing.message.subject} успешно отправлено на почту {recipient.email}"
            )
        except Exception as e:
            MailingAttempt.objects.create(
                date_attempt=timezone.now(),
                status="FA",
                mail_response=str(e),
                mailing=mailing,
            )
            print(str(e))

    if successful_attempts > 0:
        mailing.status = Mailing.LAUNCHED
        if not mailing.first_dispatch:
            mailing.first_dispatch = timezone.now()

    mailing.save()


class Command(BaseCommand):
    help = "Send messages"

    def handle(self, *args, **kwargs):
        messages = Mailing.objects.filter(status__in=["CR", "LA"])
        for mailing in messages:
            send_mailing(mailing)
