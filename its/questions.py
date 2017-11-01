# -*- coding: utf-8 -*-
from .models import *
from django.conf import settings
import telepot
import json
from collections import deque
from random import shuffle
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from textwrap import dedent
from .messages import *
TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)


def text_answer_handler(msg):
    chat_id = msg['chat']['id']
    data = msg['text']
    user_id = msg['from']['id']
    # try:
    answer_handler(chat_id, user_id, data)
    # except Exception:
    #     clear(msg)


def callback_answer_handler(msg):
    TelegramBot.answerCallbackQuery(callback_query_id = msg['callback_query']['id'])
    chat_id = msg['callback_query']['message']['chat']['id']
    user_id = msg['callback_query']['from']['id']
    data = msg['callback_query']['data']
    # try:
    answer_handler(chat_id, user_id, data)
    # except Exception:
    #     clear(msg)


def answer_handler(chat_id, user_id, data):
    user = User.objects.get(id = user_id)
    online_session = user.online_session
    question_list = online_session.question_list.split()
    question_num = online_session.current_question_num
    question = online_session.current_questions.get(id = question_list[question_num - 1])
    complexity = question.complexity
    online_session.current_questions.remove(question)
    mask = online_session.mask.split()
    online_session.save()

    session = online_session.session
    top = session.top_border
    bottom = session.bottom_border



    if check_answer(data, question):
        online_session.user_result += int(question.complexity)
    else:
        while (online_session.current_questions.filter(complexity = complexity).count() == 0):
            complexity -= 1
            if complexity == 0:
                break
        else:
            mask.insert(0, str(complexity))
            online_session.mask = " ".join(mask)

    message = answer_message.format(
                                    data,
                                    Answer.objects.get(question = question).text,
                                    online_session.user_result,
                                    )
    TelegramBot.sendMessage(chat_id, dedent(message).decode("utf-8"))
    online_session.save()

    if online_session.current_question_num == top or (online_session.user_result >= session.limit_sum and online_session.current_question_num >= bottom):
        TelegramBot.sendMessage(chat_id, "Тест закончен")
        user.online_session = None
        user.save()
        online_session.current_questions.clear()
        online_session.delete()
        online_session.save()
    else:
        try:
            online_session.current_question_num = question_num + 1
            online_session.save()
            ask_question(chat_id, user_id)
        except Exception:
            TelegramBot.sendMessage(chat_id, "Вопрос не задан. Что-то пошло не так")
            raise



def check_answer(answer, question):
        if str(answer) == str(Answer.objects.get(question = question).text.encode("utf-8")):
            return True
        else:
            return False


def make_mask(session):
    bottom = session.bottom_border
    mask = []
    for i in range(1, 6):
        mask += [i] * bottom // 5
    for i in range(1, bottom % 5):
        mask += [i]
    return " ".join(mask.sort())

def ask_question(chat_id, user_id):
    user = User.objects.get(id = user_id)
    online_session = user.online_session
    mask = online_session.mask.split()
    question_list = online_session.question_list.split()
    complexity = online_session.mask[0]
    session = online_session.session
    new_questions = online_session.current_questions.filter(complexity = mask.pop(0))
    question = new_questions.first()
    question_list.append(str(question.id))
    online_session.mask = " ".join(mask)
    online_session.question_list = " ".join(question_list)
    online_session.save()
    message = question_message.format(online_session.current_question_num, question.text, complexity)
    if question.answers:
        answers = question.answers.split(" ")
        keyboard = []
        for answer in answers:
            keyboard.append([InlineKeyboardButton(text = answer, callback_data = answer)])
        keyboard = InlineKeyboardMarkup(inline_keyboard = keyboard)
        TelegramBot.sendMessage(chat_id, dedent(message).decode("utf-8"), reply_markup=keyboard)
    else:
        TelegramBot.sendMessage(chat_id, dedent(message).decode("utf-8"))
