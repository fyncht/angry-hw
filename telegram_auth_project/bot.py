from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

DJANGO_SERVER = "http://127.0.0.1:8000"

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    username = update.effective_user.username

    response = requests.get(f"{DJANGO_SERVER}/callback/", params={
        'telegram_id': telegram_id,
        'username': username,
    })

    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")

    if response.status_code == 200:
        auth_url = f"{DJANGO_SERVER}/auth_complete/?token={response.json().get('token')}"
        await update.message.reply_text(f"Вы успешно авторизовались! Перейдите на сайт: {auth_url}")
    else:
        await update.message.reply_text(f"Ошибка авторизации: {response.text}")


def main():
    BOT_TOKEN = "7256196596:AAHbHFMvFoZDhMvGhnljUkaop5MItiU-L4A"

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == '__main__':
    main()
