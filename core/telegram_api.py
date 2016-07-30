import urllib
import requests

from asl import settings

def invoke_telegram(method, **kwargs):
    url = "https://api.telegram.org/bot%s/%s?%s" % (settings.TELEGRAM_BOT_TOKEN, method, urllib.urlencode(kwargs))
    resp = requests.get(url)
    return resp