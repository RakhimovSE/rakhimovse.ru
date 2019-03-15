from telegram import InlineQueryResultArticle, InputTextMessageContent


def start(bot, update, args=None):
    text = ' '.join(args) if args else 'Привет!'
    bot.send_message(chat_id=update.message.chat_id, text=text)


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def count(bot, update, args):
    chat_id = update.message.chat_id
    try:
        n = int(args[0])
    except:
        bot.send_message(chat_id=chat_id, text='Введи число после команды')
        return
    else:
        bot.send_message(chat_id=chat_id, text='Начинаем считать барашков')
    for i in range(n):
        bot.send_message(chat_id=chat_id, text='{} барашек'.format(i + 1))
    bot.send_message(chat_id=chat_id, text='Закончили считать барашков')


def caps(bot, update, args):
    text = ' '.join(args).upper() or 'Напиши текст после команды'
    bot.send_message(chat_id=update.message.chat_id, text=text)


def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper()),
        ),
    ]
    bot.answer_inline_query(update.inline_query.id, results)


def sticker(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='И что мне делать с твоим стикером?')


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Не найдена указанная команда')
