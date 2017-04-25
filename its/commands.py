from .models import Session, Question
from django.conf import settings
import telepot
import json
from collections import deque
from random import shuffle
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
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
    TelegramBot.answerCallbackQuery(callback_query_id = msg['callback_query']['id'])
    chat_id = msg['callback_query']['chat']['id']
    data = msg['callback_query']['data']
    queue = json.loads(data)
    if (len(queue)!=0):
        ask_question(chat_id, queue)
    else:
        TelegramBot.sendMessage(chat_id, "Тест закончен")



def test_session(chat_id):
    session= Session.objects.get(id = 1)
    top = session.top_border
    bottom = session.bottom_border
    questions = session.questions

    queue = deque(questions.all())
    shuffle(queue)
    ask_question(queue)


def ask_question(chat_id, queue):
    question = queue.popleft()
    answers = question.asnwers.split(", ")
    text = question.text
    data = json.dump(queue, skipkeys = True)
    if not answers:
        keyboard = []
        for asnwer in answers:
            keyboard.append(InlineKeyboardButton(text = answer, data = data))
        keyboard = InlineKeyboardMarkup(inline_keyboard = keyboard)
    TelegramBot.sendMessage(chat_id, text, reply_markup=keyboard)
