from telegram import Bot, Update


def start(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text='Yolo')


def echo(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def sticker(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text='И что мне делать с твоим стикером?')
