from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import TelegramUser
from django.http import JsonResponse


def index(request):
    user = request.user
    return render(request, 'auth_app/index.html', {'user': user})


def login_with_telegram(request):
    bot_username = "angry_auth_bot"
    unique_token = "jopa"
    callback_url = f"https://t.me/{bot_username}?start={unique_token}"

    request.session['login_token'] = unique_token
    return redirect(callback_url)


def telegram_callback(request):
    token = request.GET.get('token')
    telegram_id = request.GET.get('telegram_id')
    username = request.GET.get('username')

    if not token or not telegram_id or not username:
        return JsonResponse({'error': 'Invalid data'}, status=400)

    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_unusable_password()
        user.save()

    login(request, user)

    return redirect('/')
