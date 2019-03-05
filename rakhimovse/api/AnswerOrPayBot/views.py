from rest_framework.response import Response
from rest_framework.decorators import api_view
from telegram import Update

from rakhimovse.api.AnswerOrPayBot.apps import AnswerorpaybotConfig


@api_view(['POST'])
def webhook(request):
    update = Update.de_json(request.data, AnswerorpaybotConfig.dispatcher.bot)
    AnswerorpaybotConfig.dispatcher.process_update(update)
    return Response()
