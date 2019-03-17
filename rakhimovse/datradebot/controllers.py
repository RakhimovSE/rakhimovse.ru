from django.db import transaction
from datetime import datetime
import logging
from rakhimovse.datradebot import keyboards


def send_start_message(update, context):
    user, created = get_or_create_user(update.message, context.args)
    if created and user.inviter:
        try:
            context.bot.send_message(user.inviter.id, 'Поздравляем! У вас новый реферал')
        except:
            pass
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Привет, {}!'.format(user.first_name),
        reply_markup=keyboards.get_main_menu_keyboard(),
    )


def edit_menu_callback(update, context, text, keyboard, **kwargs):
    message = update.callback_query.message
    context.bot.edit_message_text(
        text=text,
        chat_id=message.chat_id,
        message_id=message.message_id,
        reply_markup=keyboard,
        **kwargs,
    )
    context.bot.answer_callback_query(update.callback_query.id)


def get_or_create_user(message, args=None):
    from rakhimovse.datradebot.models import User

    kwargs = {
        'id': message.chat.id,
        'username': message.chat.username,
        'first_name': message.chat.first_name,
        'last_name': message.chat.last_name,
    }
    try:
        user = User.objects.get(id=kwargs['id'])
        created = False
    except User.DoesNotExist:
        try:
            user = User.objects.create(**kwargs, inviter_id=int(args[0]))
        except:
            user = User.objects.create(**kwargs)
        created = True
    return user, created


def accept_payment(bot, user, amount):
    invite_percent_lines = [10, 9, 8, 7, 6]
    inviters = []
    inviter = user.inviter
    for percent in invite_percent_lines:
        if not inviter:
            break
        inviter.wallet += amount / 100 * percent
        inviters.append(inviter)
        inviter = inviter.inviter
    with transaction.atomic():
        for inviter in inviters:
            inviter.save()
    for inviter in inviters:
        text = 'Вы получили начисление по реферальной системе!\n' \
               'Текущий баланс: {}'.format(inviter.wallet)
        try:
            bot.send_message(chat_id=inviter.id, text=text)
        except Exception as exc:
            logging.error(exc)


def activate_promo(update, context):
    from rakhimovse.datradebot.models import Promo

    error_text = ''
    try:
        promo = Promo.objects.get(id=update.message.text.upper())
    except Promo.DoesNotExist:
        error_text = 'Промокод не найден'
    else:
        if not promo.is_active:
            error_text = 'Промокод уже не действителен'
        elif promo.subscription:
            error_text = 'Промокод уже активирован'
    if error_text:
        error_text += '\nПопробуйте еще раз или нажмите /cancel для отмены'
        context.bot.send_message(update.message.chat_id, error_text)
        return False

    user, _ = get_or_create_user(update.message)
    promo.issue(user)
    text = 'Промокод принят!\nПодписка действительна до {}'.format(
        datetime.strftime(user.subscription_active_until, '%d.%m.%Y')
    )
    context.bot.send_message(update.message.chat_id, text)
    return True
