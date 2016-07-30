import logging
import urllib
import requests

from asl import settings

logger = logging.getLogger(__name__)

def invoke_telegram(method, **kwargs):
    url = "https://api.telegram.org/bot%s/%s?%s" % (settings.TELEGRAM_BOT_TOKEN, method, urllib.urlencode(kwargs))
    logger.info("Requesting %s" % url)
    resp = requests.get(url)
    logger.info("Response %s %s" % (resp, resp.content))
    return resp
#urllib.urlencode(kwargs)