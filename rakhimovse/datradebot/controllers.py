from django.db import transaction
from django.utils.timezone import datetime
import logging


def edit_menu_callback(bot, update, text, keyboard, **kwargs):
    message = update.callback_query.message
    bot.edit_message_text(
        text=text,
        chat_id=message.chat_id,
        message_id=message.message_id,
        reply_markup=keyboard,
        **kwargs,
    )
    bot.answer_callback_query(update.callback_query.id)


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
    except User.DoesNotExist:
        try:
            user = User.objects.create(**kwargs, invited_by_id=int(args[0]))
        except:
            user = User.objects.create(**kwargs)
    return user


def accept_payment(bot, user, amount):
    invite_percent_lines = [10, 9, 8, 7, 6]
    inviters = []
    inviter = user.invited_by
    for percent in invite_percent_lines:
        if not inviter:
            break
        inviter.wallet += amount / 100 * percent
        inviters.append(inviter)
        inviter = inviter.invited_by
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


def handle_promo(bot, update):
    from rakhimovse.datradebot.models import Promo
    try:
        promo = Promo.objects.get(id=update.message.text.upper())
    except Promo.DoesNotExist:
        bot.send_message(chat_id=update.message.chat_id, text='Промокод не найден')
        return

    if not promo.is_active:
        bot.send_message(chat_id=update.message.chat_id, text='Промокод уже не действителен')
        return

    user = get_or_create_user(update.message)
    promo.issue(user)
    text = 'Промокод принят!\nПодписка действительна до {}'.format(
        datetime.strftime(user.subscription_active_until, '%d.%m.%Y')
    )
    bot.send_message(chat_id=update.message.chat_id, text=text)
