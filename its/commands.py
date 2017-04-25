from .models import Session, Question
import telepot

def handler(payload):
    if "callback_query" in payload:
        callback_handler(payload)
    if "message" in payload:
        message = payload['message']
        message_handler(message)


def message_handler(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    TelegramBot.sendMessage(chat_id, telepot.glance(msg))

def callback_handler(msg):
    pass

def start(atributes):
    TelegramBot.sendMessage(chat_id,
    "Вы запустили тестового бота.\n Пожалуйста не ломайте его,
    Я долго над ним стралася")


def session(atributes):
    if atributes[0] == "test":
        session_id = Session.objects.get(id = 0)
        questions = session_id.question


    else:
        TelegramBot.sendMessage(chat_id,
        "Сессии пока работаю только в тетстовом режиме")
    pass


def question(q):
    pass
