from django.http import HttpResponse
from telegram.bot import Bot
from telegram.ext import messagequeue as mq


class MQBot(Bot):
    """A subclass of Bot which delegates send method handling to MQ"""
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        """Wrapped method would accept new 'queued' and 'isgroup' OPTIONAL arguments"""
        return super(MQBot, self).send_message(*args, **kwargs)


ANSWERORPAYBOT_TOKEN = 'PUT_YOUR_TOKEN_HERE'
DATRADEBOT_TOKEN = 'PUT_YOUR_TOKEN_HERE'


def index(request):
    return HttpResponse('Yo')
