from rakhimovse.datradebot import keyboards, controllers
from telegram.ext import ConversationHandler


TYPING_PROMO = 1


def main_menu_callback_handler(update, context):
    keyboard = keyboards.get_main_menu_keyboard()
    controllers.edit_menu_callback(update, context, 'Главное меню', keyboard)


def partner_menu_callback_handler(update, context):
    keyboard = keyboards.get_partner_menu_keyboard()
    controllers.edit_menu_callback(update, context, 'Меню "Партнёрство"', keyboard)


def payment_menu_callback_handler(update, context):
    keyboard = keyboards.get_payment_menu_keyboard()
    controllers.edit_menu_callback(update, context, 'Меню "Стоимость"', keyboard)


def settings_menu_callback_handler(update, context):
    keyboard = keyboards.get_settings_menu_keyboard()
    controllers.edit_menu_callback(update, context, 'Меню "Настройки"', keyboard)


def about_us_callback_handler(update, context):
    context.bot.answer_callback_query(update.callback_query.id, '"Про нас"')


def faq_callback_handler(update, context):
    context.bot.answer_callback_query(update.callback_query.id, '"FAQ"')


def promo_callback_handler(update, context):
    context.bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text='Введите промокод или нажмите /cancel для отмены',
    )
    context.bot.answer_callback_query(update.callback_query.id)
    return TYPING_PROMO


def typing_promo_message_handler(update, context):
    success = controllers.activate_promo(update, context)
    if success:
        controllers.send_start_message(update, context)
        return ConversationHandler.END


def cancel_command_handler(update, context):
    controllers.send_start_message(update, context)
    return ConversationHandler.END


def unknown_callback_handler(update, context):
    context.bot.answer_callback_query(update.callback_query.id, 'В разработке')


def start_command_handler(update, context):
    controllers.send_start_message(update, context)


def unknown_message_handler(update, context):
    context.bot.send_message(update.message.chat_id, 'Не найдена указанная команда')
    controllers.send_start_message(update, context)
