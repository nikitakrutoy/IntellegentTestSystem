from .models import Session, Question
from django.conf import settings
import telepot
from collections import deque

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
    if "entities" in msg:
        entities = msg["entities"]
        if entities[0]["type"] == "bot_command":
            if msg["text"] == "/session":
                test_session(chat_id)


def callback_handler(msg):
    chat_id = msg['callback_query']['chat']['id']
    TelegramBot.sendMessage(chat_id, msg)



def test_session(chat_id):
    if atributes[0] == "test":
        session= Session.objects.get(id = 0)
        top = session.top_border
        bottom = session.bottom_border
        questions = session.question
        queue = deque(questions)
        TelegramBot.sendMessage(chat_id, queue)


def question(q):
    pass
