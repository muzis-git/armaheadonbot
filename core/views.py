from django.shortcuts import render
import json
import urllib
import time

import requests

from core.telegram_api import invoke_telegram
from models import TelegramChat
from django.views.decorators.csrf import csrf_exempt
from asl import settings


from django.http import HttpResponse
# Create your views here.


@csrf_exempt
def telegram_hook(request):
    update = json.loads(request.body)
    message = update['message']
    tc, created = TelegramChat.objects.get_or_create(chat_id=message['chat']['id'])
    if created:
        tc.username = message['chat']['username']
        tc.save()
    if '/' in message['text'][0]:
        telegram_commands(message, request)
    elif "I'm on" in message['text']:
        telegram_duty(message)
    elif "I'm" in message['text']:
        telegram_emotion(message)


def init(request):
    invoke_telegram('setWebhook', url=settings.TELEGRAM_HOOK_URL)

    return HttpResponse('OK')


def telegram_alert(request, username):
    message = request.GET.get('message')
    message = urllib.unquote_plus(message)\

    j = json.loads(message)
    text = '%s %s %s' % (j['checkname'], j['description'], j['incidentid'])

    _send_telegram_by_username(username, text)

    return HttpResponse('OK')


def _send_telegram_by_username(username, text):
    lst = TelegramChat.objects.filter(username=username)
    if len(lst) == 0:
        raise Exception("Could not find chat by username %s" % username)

    for c in lst:
        resp = invoke_telegram('sendMessage', text=text.encode('utf-8'), chat_id=c.chat_id)

def send_telegram(request, username):
    _send_telegram_by_username(username, request.GET.get('text'))
    return HttpResponse('OK')


def telegram_commands(message, request):
    commands = {'help','start','song','set'}
    if message['text'][1:] not in commands:
        resp = invoke_telegram('sendMessage', text='Command does not exist', chat_id=message['chat']['id'])
    elif message['text'][1:] == 'song':
        _send_telegram_by_username(message['chat']['username'],'Name the song')
        c = message['chat']['id']
        update = json.loads(request.body)
        message = update['message']
        update = json.loads(requests.post('http://muzis.ru/api/search.api?q_track',data= message['text']))
        message = update['message']
        invoke_telegram('sendVoice', audio=message['songs']['file_mp3'],chat_id=c)
    elif message['text'][1:] == 'set':
        _send_telegram_by_username(message['chat']['username'], 'Every ? hours post recomended music?')
        c = message['chat']['id']
        update = json.loads(request.body)
        message = update['message']
        _send_telegram_by_username(message['chat']['username'],'Timer set')
        time.sleep(int(message['text'])*3600)
        update = json.loads(requests.post('http://muzis.ru/api/search.api?q_value=25201?value=5'))
        message = update['message']
        invoke_telegram('sendVoice', audio=message['songs']['file_mp3'], chat_id=c)


def telegram_emotion(message):
    c = message['chat']['id']
    if 'sad' in message['text']:
        update = json.loads(requests.post('http://muzis.ru/api/search.api?q_value=25201?value=5'))
        message = update['message']
        invoke_telegram('sendVoice', audio=message['songs']['file_mp3'], chat_id=c)
    elif 'happy' in message['text']:
        update = json.loads(requests.post('http://muzis.ru/api/search.api?q_value=25739?value=5'))
        message = update['message']
        invoke_telegram('sendVoice', audio=message['songs']['file_mp3'], chat_id=c)


def telegram_duty(message):
    c = message['chat']['id']
    if 'work' in message['text']:
        update = json.loads(requests.post('http://muzis.ru/api/search.api?q_value=25201?value=5'))
        message = update['message']
        invoke_telegram('sendVoice', audio=message['songs']['file_mp3'], chat_id=c)
    elif 'gym' in message['text']:
        update = json.loads(requests.post('http://muzis.ru/api/search.api?q_value=25739?value=5'))
        message = update['message']
        invoke_telegram('sendVoice', audio=message['songs']['file_mp3'], chat_id=c)