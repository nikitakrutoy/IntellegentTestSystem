from .models import Session, Question, User
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
    user = User.objects.get(user_id = 0)
    queue = user.current_session_questions
    currnet_question = queue.pop()
    user.current_session_questions = ','.join(queue);
    user.save()
    if (len(queue)!=0):
        ask_question(chat_id)
    else:
        TelegramBot.sendMessage(chat_id, "Тест закончен")



def test_session(chat_id):
    session= Session.objects.get(id = 1)
    user = User.objects.get(user_id = 0)
    user.current_session = session;
    top = session.top_border
    bottom = session.bottom_border
    queue = []
    questions_objs = session.questions.all()
    for obj in questions_objs:
        queue.append(str(obj.question_id))
    shuffle(queue)
    user.current_session_questions = ','.join(queue);
    user.save()
    ask_question(chat_id)


def ask_question(chat_id):
    user = User.objects.get(user_id = 0)
    queue = user.current_session_questions.split(',')
    question = Question.objects.get(question_id = queue[len(queue)-1])
    text = question.text
    # data = json.dump(queue, skipkeys = True)
    if question.answer:
        answers = question.asnwers.split(", ")
        keyboard = []
        for answer in answers:
            keyboard.append([InlineKeyboardButton(text = answer, callback_data = answer)])
        keyboard = InlineKeyboardMarkup(inline_keyboard = keyboard)
    TelegramBot.sendMessage(chat_id, text, reply_markup=keyboard)
