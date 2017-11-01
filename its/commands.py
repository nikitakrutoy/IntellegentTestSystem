# -*- coding: utf-8 -*-
from .models import *
from django.conf import settings
import telepot
import json
from collections import deque
from random import shuffle
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from textwrap import dedent
from .messages import *
from .session import *
TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)


def handler(payload):
    try:
        if "message" in payload:
            message = payload['message']
            if if_start(message):
                start(message)
            elif if_clear(message):
                clear(message)
            else:
                message_handler(message)
    except Exception:
        chat_id  = payload['message']['chat']['id']
        TelegramBot.sendMessage(chat_id, dedent(str(payload).decode("utf-8")))
    if "callback_query" in payload:
        callback_handler(payload)


def if_start(message):
    chat_id = message['chat']['id']
    user_id = message['from']['id']
    if "entities" in message:
        entities = message["entities"]
        if entities[0]["type"] == "bot_command" and message["text"].split()[0] == "/start":
            return True
    return False

def if_clear(message):
    chat_id = message['chat']['id']
    user_id = message['from']['id']
    if "entities" in message:
        entities = message["entities"]
        if entities[0]["type"] == "bot_command" and message["text"].split()[0] == "/clear":
            return True
    return False


def callback_handler(payload):
    chat_id = payload['callback_query']['message']['chat']['id']
    try:
        TelegramBot.answerCallbackQuery(callback_query_id = payload['callback_query']['id'])
    except Exception:
        TelegramBot.sendMessage(chat_id, dedent(str(payload).decode("utf-8")))
    message = payload['callback_query']['message']
    user_id = payload['callback_query']['from']['id']
    user = User.objects.get(id = user_id)
    data = payload['callback_query']['data']
    if user.status == 4:
        answer_handler(chat_id, user_id, data)
    else:
        status = int(data)
        if status == 10:
            help(message)
        if status == 1:
            online_session(message)
        if status == 2:
            choose_session(message)
        if status == 5:
            create(message)
        if status == 0:
            gohome(message)
        if status > 100:
            session_info(message, status-100)



def message_handler(msg):
    chat_id = msg['chat']['id']
    user_id = msg['from']['id']
    msg_id = msg['message_id']
    user = User.objects.get(id = user_id)
    status = user.status
    if status == 0: # Usual query

        if "entities" in msg:
            entities = msg["entities"]
            if entities[0]["type"] == "bot_command":
                try:
                    commands[msg["text"].split()[0]](msg)
                except KeyError:
                    TelegramBot.sendMessage(chat_id, "Такой команды нет")
        else:
            TelegramBot.sendMessage(chat_id, "Воспользуйтесь меню ✅", parse_mode = "Markdown")
    if status == 1:
        start_session(msg)
    if status == 2: # Creating
        try:
            test_name, questions_num, mistakes_num = msg['text'].split()
        except ValueError:
            TelegramBot.sendMessage(chat_id, dedent("Недостаточно аргументов. Попробуйте еще раз".decode("utf-8")))
            return
        session = user.created_sessions.create()
        session.name = test_name
        session.bottom_border = int(questions_num)
        session.top_border = int(questions_num) + int(mistakes_num)
        session.limit_sum = sum([i for i in range(int(questions_num)+1)])
        session.save()
        TelegramBot.sendMessage(chat_id, dedent(created.format(
                                                                session.name,
                                                                session.id)))
        user.status = 0
        user.save()
    if status > 100: # Adding question
        data = msg['text'].split('\n')
        session_id = status - 100
        session = Session.objects.get(id = session_id)
        author = session.user_set.all().first()
        if author.id != int(user_id):
            TelegramBot.sendMessage(chat_id, "Вы не можете редактировать этот тест!")
        questions = data
        for i in range(0, len(questions)):
            question = Question()
            answer = Answer()
            temp = questions[i].split("-")
            if len(temp) == 3 and i < session.bottom_border:
                question.text, answers, right_answer = temp
                question.complexity = i + 1
            elif len(temp) == 4:
                question.text, answers, right_answer, complexity = questions[i].split("-")
                question.complexity = complexity
            else:
                TelegramBot.sendMessage(chat_id, "Недостаточно аргументов. Попробуйте еще раз.")
                return
            answers = answers.split(",")
            if len(answers) > 1:
                question.answers = ",".join(answers)
            question.author = user
            question.save()
            answer.text = right_answer
            answer.question = question
            session.questions.add(question)
            question.save()
            answer.save()
        session.save()
        TelegramBot.sendMessage(user_id, dedent(added).decode("utf-8"))
        user.status = 0
        TelegramBot.deleteMessage((chat_id, user.menu_msg_id))
        menu_msg = TelegramBot.sendMessage(chat_id, dedent(home).decode("utf-8"), reply_markup = home_keyboard)
        user.menu_msg_id = menu_msg['message_id']
        user.save()
    if status == 4:
        data = msg['text']
        answer_handler(chat_id, user_id, data)

def text_answer_handler(msg):
    chat_id = msg['chat']['id']
    data = msg['text']
    user_id = msg['from']['id']
    # try:
    answer_handler(chat_id, user_id, data)
    # except Exception:
    #     clear(msg)

def answer_handler(chat_id, user_id, data):
    user = User.objects.get(id = user_id)
    online_session = user.online_session
    question_list = online_session.question_list.split()
    answer_list = online_session.answers_list.split()
    right_list = online_session.right_list.split()
    question_num = online_session.current_question_num
    try :
        question = online_session.current_questions.get(id = question_list[question_num - 1])
    except Exception:
        return
    complexity = question.complexity
    online_session.current_questions.remove(question)
    msg_id = online_session.msg_id
    mask = online_session.mask.split()
    online_session.save()

    session = online_session.session
    top = session.top_border
    bottom = session.bottom_border

    answer_list.append(data)
    online_session.answers_list = " ".join(answer_list)
    online_session.save()
    if check_answer(data, question):
        online_session.user_result += int(question.complexity)
        right_list.append("1")

    else:
        right_list.append("0")
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
    online_session.right_list = " ".join(right_list)
    online_session.save()

    if online_session.current_question_num == top or (online_session.user_result >= session.limit_sum and online_session.current_question_num >= bottom):
        resultq = "<b>Тест закончен</b>\n".decode("utf-8")
        for i in range(len(question_list)):
            question_id = question_list[i]
            temp_question = Question.objects.get(id = question_id).text
            temp_answer = answer_list[i]
            is_right = right_list[i]
            if is_right == "1":
                is_right = u"✅"
            else:
                is_right = u"❌"
            resultq += dedent(result_questions.format(str(i+1).decode("utf-8"), temp_question, temp_answer, is_right))
        max_mark = float(session.limit_sum)/session.bottom_border
        mark = float(online_session.user_result)/question_num
        mark = (float(mark) / float(max_mark)) * 10
        resultq += dedent(result.format(mark))
        TelegramBot.editMessageText((chat_id, msg_id), resultq, parse_mode="HTML")
        online_session.current_questions.clear()
        user.online_session = None
        user.status = 0
        TelegramBot.deleteMessage((chat_id, user.menu_msg_id))
        menu_msg = TelegramBot.sendMessage(chat_id, dedent(home).decode("utf-8"), reply_markup = home_keyboard)
        user.menu_msg_id = menu_msg['message_id']
        user.save()
        online_session.delete()
    else:
        try:
            online_session.current_question_num = question_num + 1
            online_session.save()
            ask_question(chat_id, user_id)
        except Exception:
            TelegramBot.sendMessage(chat_id, "Вопрос не задан. Что-то пошло не так")
            raise


def start(msg):
    chat_id = msg['chat']['id']
    user_id = msg['from']['id']

    if 'username' in msg['from']:
        telegram_name = msg['from']['username']
    else:
        telegram_name = None
    if (User.objects.filter(id = user_id).count() == 0):
        user = User(id = user_id, telegram_name = telegram_name)
        menu_msg = TelegramBot.sendMessage(chat_id, dedent(home).decode("utf-8"), reply_markup = home_keyboard)
        user.menu_msg_id = menu_msg['message_id']
        user.save()
    else:
        TelegramBot.sendMessage(chat_id, "Вы уже добавлены")


def online_session(msg):
    chat_id = msg['chat']['id']
    user_id = chat_id
    user = User.objects.get(id = user_id)
    msg_id = user.menu_msg_id
    user.status = 1
    user.save()
    TelegramBot.editMessageText((chat_id, msg_id), text = "Введите номер теста", reply_markup = backhome_keyboard)



def start_session(msg):
    chat_id = msg['chat']['id']
    try:
        session_id = int(msg['text'])
    except Exception:
        TelegramBot.sendMessage(chat_id, "id это число", parse_mode="HTML")
        return
    user_id = msg['from']['id']
    msg_id = msg['message_id']
    try:
        initiate_session(chat_id, user_id, session_id)
    except Exception:
        return
    user = User.objects.get(id = user_id)
    user.status = 4;
    user.save()
    ask_question(chat_id, user_id)


def clear(msg):
    user_id = msg['chat']['id']
    user = User.objects.get(id = user_id)
    online_session = user.online_session
    user.online_session = None
    user.status = 0
    user.save()
    if online_session:
        online_session.current_questions.clear()
        online_session.delete()
        online_session.save()
    TelegramBot.sendMessage(user_id, "Данные очищены")

def gohome(msg):
    user_id = msg['chat']['id']
    chat_id = user_id
    user = User.objects.get(id = user_id)
    online_session = user.online_session
    msg_id = user.menu_msg_id
    user.online_session = None
    user.status = 0
    user.save()
    if online_session:
        online_session.current_questions.clear()
        online_session.delete()
        online_session.save()
    TelegramBot.editMessageText((chat_id, msg_id), dedent(home).decode("utf-8"), reply_markup = home_keyboard)

def menu(msg):
    chat_id = msg['chat']['id']
    user_id = msg['chat']['id']
    user = User.objects.get(id = user_id)
    user.status = 0
    menu_msg_id = user.menu_msg_id
    try:
        TelegramBot.deleteMessage((chat_id, menu_msg_id))
    except Exception:
        TelegramBot.sendMessage(chat_id, "Не получилось удалить предыдущее меню".decode("utf-8"))
    menu_msg = TelegramBot.sendMessage(chat_id, dedent(home).decode("utf-8"), reply_markup = home_keyboard)
    user.menu_msg_id = menu_msg['message_id']
    user.save()


def create(msg):
    user_id = msg['chat']['id']
    user = User.objects.get(id = user_id)
    user.status = 2; # Creating
    user.save()
    msg_id = user.menu_msg_id
    TelegramBot.editMessageText((user_id, msg_id), dedent(create_test).decode("utf-8"), reply_markup = backhome_keyboard)


def add(msg):
    session_id = msg['text'].split()[1]
    user_id = msg['chat']['id']
    user = User.objects.get(id = user_id)
    session = Session.objects.get(id = session_id)
    user.status = 3 # Adding
    user.save()
    TelegramBot.sendMessage(user_id, dedent(add_questions.format(session.bottom_border,
    session.top_border - session.bottom_border,
    session.bottom_border + 1)).decode("utf-8"))

def choose_session(msg):
    chat_id = msg['chat']['id']
    user_id = msg['chat']['id']
    user = User.objects.get(id = user_id)
    msg_id = user.menu_msg_id
    session_list_keyboard = []
    user_sessions = user.created_sessions.all()
    if user_sessions.count() == 0:
        menu_msg = TelegramBot.editMessageText((chat_id, msg_id), dedent(not_create).decode("utf-8"), reply_markup = create_keyboard)
    else:
        for s in user_sessions:
            sbutton = InlineKeyboardButton(text=s.name+": " + str(s.id).decode("utf-8"), callback_data = str(100+s.id).decode("utf-8"))
            session_list_keyboard.append([sbutton])
        session_list_keyboard.append([InlineKeyboardButton(text="Создать тест", callback_data = "5")])
        session_list_keyboard.append([InlineKeyboardButton(text="Домой", callback_data = "0")])
        session_list_keyboard = InlineKeyboardMarkup(inline_keyboard = session_list_keyboard)
        TelegramBot.editMessageText((chat_id, msg_id), dedent(choose_text).decode("utf-8"), reply_markup = session_list_keyboard, parse_mode = "HTML")

def session_info(msg, session_id):
    chat_id = msg['chat']['id']
    user_id = msg['chat']['id']
    user = User.objects.get(id = user_id)
    msg_id = user.menu_msg_id
    session = Session.objects.get(id = session_id)
    questions = session.questions.all()
    if questions.count() == 0:
        user.status = 100 + session_id
        user.save()
        TelegramBot.editMessageText((chat_id, msg_id), dedent(add_questions.format(session.bottom_border,
        session.top_border - session.bottom_border,
        session.bottom_border + 1)).decode("utf-8"), reply_markup = backhome_keyboard)
    else:
        message = dedent(test_message.format(session.name, session.top_border, str(session.bottom_border).decode("utf-8"), str(session.limit_sum).decode("utf-8")))
        for question in questions:
            answer = Answer.objects.get(question = question)
            message += dedent(question_message_full.format(question.text, str(question.complexity).decode("utf-8"), question.answers, answer.text))
        TelegramBot.editMessageText((chat_id, msg_id), message, reply_markup = backhome_keyboard)

def ls(msg):
    pass


def help(msg):
    chat_id = msg['chat']['id']
    user_id = msg['chat']['id']
    user = User.objects.get(id = user_id)
    msg_id = user.menu_msg_id
    TelegramBot.editMessageText((chat_id, msg_id), dedent(help_message).decode("utf-8"), reply_markup = backhome_keyboard)


commands = {
"/test" : start_session,
"/start" : start,
"/clear" : clear,
"/create" : create,
"/add": add,
"/list": ls,
"/help": help,
"/menu": menu
}
