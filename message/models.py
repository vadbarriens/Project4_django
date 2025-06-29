from django.db import models

from users.models import User


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='message_owner',
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['subject']

    def __str__(self):
        return self.subject
