from django.shortcuts import render
import environ
import json
import logging
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Press me', callback_data='press')],
               ])

    bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')


@csrf_exempt
def reply(request, bot_token):
    if bot_token != settings.TELEGRAM_BOT_TOKEN:
        return HttpResponseForbidden('Invalid token')

    raw = request.body.decode('utf-8')
    logger.info(raw)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Press me', callback_data='press')],
               ])

    payload = json.loads(raw)
    message = payload['message']
    # if "enteties" in message:
    #     if message["enteties"][0]["type"] == "bot_command":
    #         exec_command(message['text'])
    chat_id = payload['message']['chat']['id']
    TelegramBot.sendMessage(chat_id, telepot.flavor(payload))
    TelegramBot.sendMessage(chat_id, Question.objects.get(question_id = 0).text,
     reply_markup=keyboard)
    bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
    return JsonResponse({}, status=200)
