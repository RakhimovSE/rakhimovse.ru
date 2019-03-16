import logging

from django.apps import AppConfig
from telegram import Bot
from telegram.ext import (
    Dispatcher,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    Filters,
)

import rakhimovse.datradebot.handlers as h
from rakhimovse.telegram_bot import DATRADEBOT_TOKEN


class DatradebotConfig(AppConfig):
    name = 'rakhimovse.datradebot'
    dispatcher = None

    def ready(self):
        print('Launching {}'.format(DatradebotConfig.name))

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
        )

        bot = Bot(DATRADEBOT_TOKEN)
        bot.set_webhook('https://rakhimovse.ru/{}'.format(DATRADEBOT_TOKEN))
        dispatcher = Dispatcher(bot, None, workers=0)
        bot_handlers = [
            CommandHandler('start', h.start_command_handler, pass_args=True),
            CallbackQueryHandler(h.main_menu_callback_handler, pattern=r'^main:menu$'),
            CallbackQueryHandler(h.partner_menu_callback_handler, pattern=r'^partner:menu$'),
            CallbackQueryHandler(h.payment_menu_callback_handler, pattern=r'^payment:menu$'),
            CallbackQueryHandler(h.about_us_callback_handler, pattern=r'^about_us$'),
            CallbackQueryHandler(h.faq_callback_handler, pattern=r'^faq$'),
            ConversationHandler(
                entry_points=[CallbackQueryHandler(h.promo_callback_handler, pattern=r'^promo$')],
                states={
                    h.TYPING_PROMO: [MessageHandler(Filters.text, h.typing_promo_message_handler)]
                },
                fallbacks=[],
            ),
            CallbackQueryHandler(h.settings_menu_callback_handler, pattern=r'^settings:menu$'),
            CallbackQueryHandler(h.unknown_callback_handler, pattern=r''),
            MessageHandler(Filters.text | Filters.command, h.unknown_message_handler),
        ]
        [dispatcher.add_handler(handler) for handler in bot_handlers]

        DatradebotConfig.dispatcher = dispatcher
