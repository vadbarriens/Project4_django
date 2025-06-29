from django.db import models
from django.utils import timezone

from message.models import Message
from recipient.models import Recipient
from users.models import User


class Mailing(models.Model):
    COMPLETED = 'CO'
    CREATED = 'CR'
    LAUNCHED = 'LA'

    STATUS_CHOICES = {
        COMPLETED: 'Завершена',
        CREATED: 'Создана',
        LAUNCHED: 'Запущена',
    }

    first_dispatch = models.DateTimeField(verbose_name='Дата и время первой отправки', help_text='yyyy-mm-dd 00:00:00', null=True,
        blank=True)
    end_dispatch = models.DateTimeField(verbose_name='Дата и время окончания отправки', help_text='yyyy-mm-dd 00:00:00', null=True,
        blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус', default=CREATED)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', related_name='message')
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатели', related_name='recipients')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='mailing_owner',
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['status', 'first_dispatch', 'message',]
        permissions = [
            ('can_see_all_mailings', 'Can see all mailings'),
            ('can_cancel_mailing', 'Can cancel mailing'),
        ]


    def __str__(self):
        return self.status


class MailingAttempt(models.Model):
    SUCCESSFULLY = 'SU'
    FAILED = 'FA'

    STATUS_ATTEMPT_CHOICES = {
        SUCCESSFULLY: 'Успешно',
        FAILED: 'Не успешно',
    }

    date_attempt = models.DateTimeField(verbose_name='Дата и время попытки', help_text='yyyy-mm-dd 00:00:00')
    status = models.CharField(max_length=20, choices=STATUS_ATTEMPT_CHOICES, verbose_name='Статус')
    mail_response = models.TextField(verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', related_name='mailing_attempts')

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
        ordering = ['status', 'date_attempt',]

    def __str__(self):
        return f'{self.date_attempt} - {self.status}'
