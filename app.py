# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

from langconv import (
    Converter
)

from googletrans import Translator

import configparser, re, random

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

def rand_happy_sitckerid():
    stickers = ['52002734', '52002735', '52002736', '52002738', '52002742', 
                '52002743', '52002745', '52002748', '52002752', '52002768']
    r = random.randint(0, len(stickers)-1)
    return stickers[r]

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    
    msgtw = Converter('zh-hant').convert(msg)
    if msgtw != msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msgtw))
        
if __name__ == "__main__":
    app.run()