# -*- coding: utf-8 -*-
from .models import *
import telepot
from django.conf import settings
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from textwrap import dedent
from .messages import *
from random import shuffle
TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)


def check_answer(answer, question):
        if answer == Answer.objects.get(question = question).text:
            return True
        else:
            return False

def make_session(question_num, mistakes_num, user):
    session = Session()
    session.bottom_border = question_num
    session.top_border = question_num + mistakes_num
    session.limit_sum = sum([i for i in range(question_num+1)])
    session.save()
    user.created_sessions.add(session)
    user.save()
    return session



def initiate_session(chat_id, user_id, session_id):
    try:
        session = Session.objects.get(id = session_id)
    except Exception:
        TelegramBot.sendMessage(chat_id, text = "Теста c таким id не существует. Попробуйте другой", parse_mode="HTML")
        raise
    if session.questions.count() == 0:
        TelegramBot.sendMessage(chat_id, text = "В этом тесте пока нет вопросов. Попробуйте другой", parse_mode="HTML")
        raise
    user = User.objects.get(id = user_id)
    online_session = OnlineSession()
    online_session.session = session
    online_session.save()
    online_session.current_questions = session.questions.all()
    online_session.mask = make_mask(session)
    online_session.save()
    user.online_session = online_session
    online_session.save()
    user.save()
    message = test_message.format(session.name, session.top_border, session.bottom_border, session.limit_sum)
    TelegramBot.sendMessage(chat_id, dedent(message))
    session_msg = TelegramBot.sendMessage(chat_id, dedent(test_id).decode("utf-8"))
    online_session.msg_id = session_msg['message_id']
    online_session.save()

def make_mask(session):
    bottom = session.bottom_border
    mask = [str(i) for i in range(1, bottom + 1)]
    return " ".join(mask)

def ask_question(chat_id, user_id):
    user = User.objects.get(id = user_id)
    online_session = user.online_session
    mask = online_session.mask.split()
    question_list = online_session.question_list.split()
    complexity = online_session.mask[0]
    session = online_session.session
    new_questions = online_session.current_questions.filter(complexity = mask.pop(0)).order_by("?")
    question = new_questions.first()
    question_list.append(str(question.id))
    online_session.mask = " ".join(mask)
    online_session.question_list = " ".join(question_list)
    online_session.save()
    msg_id = online_session.msg_id
    message = question_message.format(online_session.current_question_num, question.text, complexity)
    if question.answers:
        answers = question.answers.split(",")
        keyboard = []
        for answer in answers:
            keyboard.append([InlineKeyboardButton(text = answer, callback_data = answer)])
        keyboard = InlineKeyboardMarkup(inline_keyboard = keyboard)
        TelegramBot.editMessageText((chat_id, msg_id), dedent(message), reply_markup=keyboard)
    else:
        TelegramBot.editMessageText((chat_id, msg_id), dedent(message))
