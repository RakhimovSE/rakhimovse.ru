import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from telegram import Update
from rakhimovse import settings

from rakhimovse.datradebot.apps import DatradebotConfig


@api_view(['POST'])
def webhook(request):
    port = request.get_port()
    if settings.DEBUG and port != '8000':
        url = 'http://127.0.0.1:8000/{}'.format(DatradebotConfig.dispatcher.bot.token)
        try:
            requests.post(url, json=request.data)
            print('Redirected to', url)
            return Response()
        except Exception as exc:
            print('Exception:', exc)
    update = Update.de_json(request.data, DatradebotConfig.dispatcher.bot)
    DatradebotConfig.dispatcher.process_update(update)
    return Response()
