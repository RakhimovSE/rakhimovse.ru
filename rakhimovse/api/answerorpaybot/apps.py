from django.apps import AppConfig
import logging
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, InlineQueryHandler, Filters


from rakhimovse.telegram_bot import ANSWERORPAYBOT_TOKEN
import rakhimovse.api.answerorpaybot.handlers as handlers


class AnswerorpaybotConfig(AppConfig):
    name = 'rakhimovse.api.answerorpaybot'
    dispatcher = None

    def ready(self):
        print('Launching {}'.format(AnswerorpaybotConfig.name))

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
        )

        bot = Bot(ANSWERORPAYBOT_TOKEN)
        bot.set_webhook('https://rakhimovse.ru/{}'.format(ANSWERORPAYBOT_TOKEN))
        dispatcher = Dispatcher(bot, None, workers=0)
        dispatcher.add_handler(CommandHandler('start', handlers.start, pass_args=True))
        dispatcher.add_handler(CommandHandler('caps', handlers.caps, pass_args=True))
        dispatcher.add_handler(CommandHandler('count', handlers.count, pass_args=True))
        dispatcher.add_handler(InlineQueryHandler(handlers.inline_caps))
        dispatcher.add_handler(MessageHandler(Filters.text, handlers.echo))
        dispatcher.add_handler(MessageHandler(Filters.sticker, handlers.sticker))
        dispatcher.add_handler(MessageHandler(Filters.command, handlers.unknown))

        AnswerorpaybotConfig.dispatcher = dispatcher
