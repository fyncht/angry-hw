from django.contrib.auth.models import User
from django.db import models


class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram_user')
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
