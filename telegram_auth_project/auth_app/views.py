from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from .models import TelegramUser
from django.http import JsonResponse

import logging
import secrets

logger = logging.getLogger(__name__)


def index(request):
    print(f"Current user: {request.user}")
    return render(request, 'auth_app/index.html')


def generate_unique_token():
    return secrets.token_urlsafe(16)


def login_with_telegram(request):
    bot_username = "angry_auth_bot"
    unique_token = generate_unique_token()
    callback_url = f"https://t.me/{bot_username}?start={unique_token}"

    request.session['login_token'] = unique_token
    return redirect(callback_url)


def telegram_callback(request):
    try:
        telegram_id = request.GET.get('telegram_id')
        username = request.GET.get('username')

        if not telegram_id or not username:
            logger.error("Missing parameters")
            return JsonResponse({"error": "Missing parameters"}, status=400)

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_unusable_password()
            user.save()

        token = get_random_string(32)
        telegram_user, _ = TelegramUser.objects.get_or_create(user=user)
        telegram_user.token = token
        telegram_user.telegram_id = telegram_id
        telegram_user.save()

        logger.info(f"Generated token for user {username}: {token}")
        return JsonResponse({"token": token}, status=200)
    except Exception as e:
        logger.error(f"Error in telegram_callback: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)


def auth_complete(request):
    token = request.GET.get('token')

    if not token:
        return redirect('/')

    telegram_user = TelegramUser.objects.filter(token=token).first()
    if telegram_user:
        login(request, telegram_user.user)
        telegram_user.token = None
        telegram_user.save()

    return redirect('/')
