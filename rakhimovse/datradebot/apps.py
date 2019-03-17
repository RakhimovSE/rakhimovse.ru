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
from coinbase.wallet.client import Client as CoinbaseClient
import rakhimovse.datradebot.handlers as h
from rakhimovse.telegram_bot import DATRADEBOT_TOKEN, COINBASE_API_KEY, COINBASE_API_SECRET


class DatradebotConfig(AppConfig):
    name = 'rakhimovse.datradebot'
    dispatcher = None  # type: Dispatcher
    coinbase_client = None  # type: CoinbaseClient

    def ready(self):
        print('Launching {}'.format(DatradebotConfig.name))

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
        )

        bot = Bot(DATRADEBOT_TOKEN)
        bot.set_webhook('https://rakhimovse.ru/{}'.format(DATRADEBOT_TOKEN))
        dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
        bot_handlers = [
            CommandHandler('start', h.start_command_handler),
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
                fallbacks=[CommandHandler('cancel', h.cancel_command_handler)],
            ),
            CallbackQueryHandler(h.settings_menu_callback_handler, pattern=r'^settings:menu$'),
            CallbackQueryHandler(
                callback=h.subscription_info_callback_handler,
                pattern=r'^subscription_info$',
            ),
            CallbackQueryHandler(h.partner_info_callback_handler, pattern=r'^partner_info$'),
            CallbackQueryHandler(h.exchange_info_callback_handler, pattern=r'^exchange_info$'),
            CallbackQueryHandler(h.unknown_callback_handler, pattern=r''),
            MessageHandler(Filters.private, h.unknown_message_handler),
        ]
        [dispatcher.add_handler(handler) for handler in bot_handlers]

        DatradebotConfig.dispatcher = dispatcher

        DatradebotConfig.coinbase_client = CoinbaseClient(
            api_key=COINBASE_API_KEY,
            api_secret=COINBASE_API_SECRET,
        )
