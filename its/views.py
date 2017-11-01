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
from commands import handler
from bot import handle

LOGGING_LEVEL = logging.DEBUG

logging.basicConfig(
    filename='bot.log',
    level=LOGGING_LEVEL,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)


@csrf_exempt
def reply(request, bot_token):
    if bot_token != settings.TELEGRAM_BOT_TOKEN:
        return HttpResponseForbidden('Invalid token')

    raw = request.body.decode('utf-8')
    logging.info(raw)
    payload = json.loads(raw)
    handler(payload)
    return JsonResponse({}, status=200)
