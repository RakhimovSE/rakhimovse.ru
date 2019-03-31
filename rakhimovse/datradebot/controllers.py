from django.db import transaction
from datetime import datetime
import logging
from django.template.loader import render_to_string
from rakhimovse.datradebot import keyboards
from rakhimovse.datradebot.helpers import CurrencyEnum


def send_start_message(message, context):
    user, created = get_or_create_user(message, context.args)
    if created and user.inviter:
        try:
            context.bot.send_message(user.inviter.id, 'Поздравляем! У вас новый реферал')
        except:
            pass
    context.bot.send_message(
        chat_id=message.chat_id,
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
        datetime.strftime(user.subscription_active_until, '%d.%m.%Y'),
    )
    context.bot.send_message(update.message.chat_id, text)
    return True


def get_subscription_info(user):
    days_left = user.subscription_days_left
    if days_left == -1:
        text = 'Подписка не активна'
    else:
        text = 'Подписка действительна до {}\nОсталось дней: {}'.format(
            datetime.strftime(user.subscription_active_until, '%d.%m.%Y'),
            user.subscription_days_left,
        )
    return text


def get_partner_info():
    return render_to_string('partner-info.wiki')


def get_about_us_info():
    return render_to_string('about-us-info.wiki')


def get_exchange_info():
    from rakhimovse.datradebot.apps import DatradebotConfig

    lines = []
    currency_pairs = [
        (CurrencyEnum.BTC, CurrencyEnum.USD),
        (CurrencyEnum.BTC, CurrencyEnum.RUB),
        (CurrencyEnum.ETH, CurrencyEnum.USD),
        (CurrencyEnum.ETH, CurrencyEnum.RUB),
    ]
    for c1, c2 in currency_pairs:
        currency_pair = '{}-{}'.format(c1, c2)
        try:
            response = DatradebotConfig.coinbase_client.get_spot_price(currency_pair=currency_pair)
            lines.append('{}: {}'.format(currency_pair, response.amount))
        except:
            pass
    return '\n'.join(lines) if lines else 'Не удалось получить информацию по курсам валют'
