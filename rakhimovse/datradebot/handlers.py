from telegram.ext import ConversationHandler
from rakhimovse.datradebot import keyboards, controllers as c


DATRADE_CHANNEL_ID = 0
TYPING_PROMO = 1


def main_menu_callback_handler(update, context):
    keyboard = keyboards.get_main_menu_keyboard()
    c.edit_menu_callback(update, context, 'Главное меню', keyboard)


def partner_menu_callback_handler(update, context):
    keyboard = keyboards.get_partner_menu_keyboard()
    c.edit_menu_callback(update, context, 'Меню "Партнёрство"', keyboard)


def payment_menu_callback_handler(update, context):
    keyboard = keyboards.get_payment_menu_keyboard()
    c.edit_menu_callback(update, context, 'Меню "Стоимость"', keyboard)


def settings_menu_callback_handler(update, context):
    keyboard = keyboards.get_settings_menu_keyboard()
    c.edit_menu_callback(update, context, 'Меню "Настройки"', keyboard)


def about_us_info_callback_handler(update, context):
    context.bot.send_message(update.callback_query.message.chat_id, c.get_about_us_info())
    c.send_start_message(update.callback_query.message, context)
    context.bot.answer_callback_query(update.callback_query.id)


def faq_callback_handler(update, context):
    context.bot.answer_callback_query(update.callback_query.id, '"FAQ"')


def promo_callback_handler(update, context):
    context.bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text='Введите промокод или /cancel для отмены',
    )
    context.bot.answer_callback_query(update.callback_query.id)
    return TYPING_PROMO


def subscription_info_callback_handler(update, context):
    user, _ = c.get_or_create_user(update.callback_query.message)
    context.bot.send_message(update.callback_query.message.chat_id, c.get_subscription_info(user))
    context.bot.answer_callback_query(update.callback_query.id)


def partner_info_callback_handler(update, context):
    chat_id = update.callback_query.message.chat_id
    context.bot.send_message(chat_id, c.get_partner_info())
    keyboard = keyboards.get_partner_menu_keyboard()
    context.bot.send_message(chat_id, 'Меню "Партнёрство"', reply_markup=keyboard)
    context.bot.answer_callback_query(update.callback_query.id)


def exchange_info_callback_handler(update, context):
    chat_id = update.callback_query.message.chat_id
    context.bot.send_message(chat_id, c.get_exchange_info())
    keyboard = keyboards.get_payment_menu_keyboard()
    context.bot.send_message(chat_id, 'Меню "Стоимость"', reply_markup=keyboard)
    context.bot.answer_callback_query(update.callback_query.id)


def ref_link_callback_handler(update, context):
    chat_id = update.callback_query.message.chat_id
    text = 'https://t.me/{}?start={}'.format(context.bot.username, chat_id)
    context.bot.send_message(chat_id, text)
    context.bot.answer_callback_query(update.callback_query.id)


def free_channel_callback_handler(update, context):
    CHANNEL_URL = 'https://t.me/joinchat/FjQ4XBdGIvQ5xQmDk66DFA'
    context.bot.send_message(update.callback_query.message.chat_id, CHANNEL_URL)
    context.bot.answer_callback_query(update.callback_query.id)


def feedback_callback_handler(update, context):
    context.bot.answer_callback_query(update.callback_query.id, '"Отзывы"')


def typing_promo_message_handler(update, context):
    success = c.activate_promo(update, context)
    if success:
        c.send_start_message(update.message, context)
        return ConversationHandler.END


def cancel_command_handler(update, context):
    c.send_start_message(update.message, context)
    return ConversationHandler.END


def unknown_callback_handler(update, context):
    context.bot.answer_callback_query(update.callback_query.id, 'В разработке')


def start_command_handler(update, context):
    c.send_start_message(update.message, context)


def unknown_message_handler(update, context):
    context.bot.send_message(update.message.chat_id, 'Не найдена указанная команда')
