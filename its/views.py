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
import .commands


TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
logger = logging.getLogger('telegram.bot')

@csrf_exempt
def reply(request, bot_token):
    if bot_token != settings.TELEGRAM_BOT_TOKEN:
        return HttpResponseForbidden('Invalid token')

    raw = request.body.decode('utf-8')
    logger.info(raw)
    payload = json.loads(raw)
    handler(payload)
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[
    #                [InlineKeyboardButton(text='Press me', callback_data='press')],
    #                [InlineKeyboardButton(text='Press me', url='https://yandex.ru/')],
    #            ])
    #
    # message = payload['message']
    # chat_id = payload['message']['chat']['id']
    # TelegramBot.sendMessage(chat_id, request)
    # TelegramBot.sendMessage(chat_id, telepot.flavor(message))
    # TelegramBot.sendMessage(chat_id, Question.objects.get(question_id = 0).text,
    #  reply_markup=keyboard)
    return JsonResponse({}, status=200)
