from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from rakhimovse.telegram_bot import token


def start(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text='Yolo')


def echo(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def sticker(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text='И что мне делать с твоим стикером?')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='AnswerOrPayBot.log',
)

dispatcher = Dispatcher(Bot(token), None, workers=0)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, echo))
dispatcher.add_handler(MessageHandler(Filters.sticker, sticker))


@api_view(['POST'])
def webhook(request):
    update = Update.de_json(request.data, dispatcher)
    dispatcher.process_update(update)
    return Response()
