from rakhimovse.datradebot import keyboards, controllers
from telegram.ext import ConversationHandler


TYPING_PROMO = 1


def main_menu_callback_handler(bot, update):
    controllers.edit_menu_callback(bot, update, 'Главное меню', keyboards.get_main_menu_keyboard())


def partner_menu_callback_handler(bot, update):
    keyboard = keyboards.get_partner_menu_keyboard()
    controllers.edit_menu_callback(bot, update, 'Меню "Партнёрство"', keyboard)


def payment_menu_callback_handler(bot, update):
    keyboard = keyboards.get_payment_menu_keyboard()
    controllers.edit_menu_callback(bot, update, 'Меню "Стоимость"', keyboard)


def settings_menu_callback_handler(bot, update):
    keyboard = keyboards.get_settings_menu_keyboard()
    controllers.edit_menu_callback(bot, update, 'Меню "Настройки"', keyboard)


def about_us_callback_handler(bot, update):
    bot.answer_callback_query(update.callback_query.id, text='"Про нас"')


def faq_callback_handler(bot, update):
    bot.answer_callback_query(update.callback_query.id, text='"FAQ"')


def promo_callback_handler(bot, update):
    bot.send_message(chat_id=update.callback_query.message.chat_id, text='Введите промокод')
    bot.answer_callback_query(update.callback_query.id)
    return TYPING_PROMO


def typing_promo_message_handler(bot, update):
    controllers.handle_promo(bot, update)
    return ConversationHandler.END


def unknown_callback_handler(bot, update):
    bot.answer_callback_query(update.callback_query.id, text='Не удалось обработать команду')


def start_command_handler(bot, update, args=None):
    user = controllers.get_or_create_user(update.message, args)
    text = ' '.join(args) if args else 'Привет, {}!'.format(user.first_name)
    markup = keyboards.get_main_menu_keyboard()
    bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=markup)


def unknown_message_handler(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Не найдена указанная команда')
