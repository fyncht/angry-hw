from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

DJANGO_SERVER = "http://127.0.0.1:8000"

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /start")
    args = context.args
    if not args:
        await update.message.reply_text("Токен отсутствует.")
        logger.error("Токен отсутствует")
        return

    token = args[0]
    telegram_id = update.effective_user.id
    username = update.effective_user.username

    logger.info(f"Получен токен: {token}, Telegram ID: {telegram_id}, username: {username}")

    response = requests.get(f"{DJANGO_SERVER}/callback/", params={
        'token': token,
        'telegram_id': telegram_id,
        'username': username,
    })

    logger.info(f"Ответ от сервера Django: {response.status_code}, {response.text}")

    if response.status_code == 200:
        await update.message.reply_text("Вы успешно вошли!")
    else:
        await update.message.reply_text("Произошла ошибка.")
        logger.error("Ошибка при запросе к Django")


def main():
    BOT_TOKEN = "7256196596:AAHbHFMvFoZDhMvGhnljUkaop5MItiU-L4A"

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == '__main__':
    main()
