from django.db import models

from users.models import User


class Recipient(models.Model):
    email = models.CharField(max_length=50, unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    comment = models.TextField(verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='recipients_owner',
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['full_name']
        permissions = [
            ('can_see_all_recipients', 'Can see all recipients'),
        ]

    def __str__(self):
        return self.full_name
