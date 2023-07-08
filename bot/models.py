from django.db import models

from core.models import CustomUser


class TgUser(models.Model):
    chat_id = models.BigIntegerField(verbose_name="id чата")
    user_ud = models.BigIntegerField(verbose_name="пользовательский идентификатор")
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Пользователь")
    verification_code = models.CharField(max_length=255, null=True, blank=True, verbose_name="Код верификации")
