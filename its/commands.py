from .models import Session, Question
from django.conf import settings
import telepot
from collections import deque
from random import shuffle
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
    session= Session.objects.get(id = 1)
    top = session.top_border
    bottom = session.bottom_border
    questions = session.questions

    queue = deque(questions.all())
    shuffle(queue)
    for question in queue:
        TelegramBot.sendMessage(chat_id, question.text)


def question(q):
    pass
