from rest_framework.response import Response
from rest_framework.decorators import api_view
from telegram import Update

from rakhimovse.datradebot.apps import DatradebotConfig


@api_view(['POST'])
def webhook(request):
    update = Update.de_json(request.data, DatradebotConfig.dispatcher.bot)
    DatradebotConfig.dispatcher.process_update(update)
    return Response()
