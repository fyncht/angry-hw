# Generated by Django 4.1.11 on 2024-12-03 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='username',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='token',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]