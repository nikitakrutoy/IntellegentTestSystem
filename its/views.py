from django.shortcuts import render
import environ
import json
import logging
import telepot
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')

def reply(request, bot_token):
    if bot_token != settings.TELEGRAM_BOT_TOKEN:
        return HttpResponseForbidden('Invalid token')

    raw = request.body.decode('utf-8')
    logger.info(raw)
    
    payload = json.loads(raw)
    chat_id = payload['message']['chat']['id']
    TelegramBot.sendMessage(chat_id, "Hello!")
    return JsonResponse({}, status=200)
