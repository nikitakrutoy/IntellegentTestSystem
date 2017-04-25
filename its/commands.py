from .models import Session, Question
from django.conf import settings
import telepot

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

def handler(payload):
    if "callback_query" in payload:
        callback_handler(payload)
    if "message" in payload:
        message = payload['message']
        message_handler(message)


def message_handler(msg):
    chat_id = msg['chat']['id']
    TelegramBot.sendMessage(chat_id, msg)

def callback_handler(msg):
    chat_id = msg['callback_query']['chat']['id']
    TelegramBot.sendMessage(chat_id, msg)



def session(atributes):
    if atributes[0] == "test":
        session_id = Session.objects.get(id = 0)
        questions = session_id.question
    pass


def question(q):
    pass
