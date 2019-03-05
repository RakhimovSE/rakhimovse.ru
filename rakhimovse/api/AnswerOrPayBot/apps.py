from django.apps import AppConfig
import logging
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from rakhimovse.telegram_bot import token
import rakhimovse.api.AnswerOrPayBot.handlers as handlers


class AnswerorpaybotConfig(AppConfig):
    name = 'rakhimovse.api.AnswerOrPayBot'
    dispatcher = None

    def ready(self):
        print('Launching {}'.format(AnswerorpaybotConfig.name))

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
            filename='AnswerOrPayBot.log',
        )

        dispatcher = Dispatcher(Bot(token), None, workers=0)
        dispatcher.add_handler(CommandHandler('start', handlers.start))
        dispatcher.add_handler(MessageHandler(Filters.text, handlers.echo))
        dispatcher.add_handler(MessageHandler(Filters.sticker, handlers.sticker))

        AnswerorpaybotConfig.dispatcher = dispatcher
