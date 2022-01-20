# -*- coding: utf-8 -*- !/usr/bin/env python
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
 
from __future__ import unicode_literals
import RPi.GPIO as GPIO
import time
import requests
import json
import errno
import random
import os
import sys
import subprocess
import tempfile
from argparse import ArgumentParser
 
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)
 
app = Flask(__name__)
 
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
 
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
 
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
 
 
# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise
 
 
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



def main(message):
    user_id = "自身のMessagingAPIのユーザーID"

    messages = TextSendMessage(text=message)
    line_bot_api.push_message(user_id, messages=messages)

message = "コマンド一覧\n・モーションカメラ\n・CPU温度\n・じゃんけん\n・カチューシャ\n・人感センサー\n・カメラ"
main(message)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    if text == 'モーションカメラ':
        buttons_template = ButtonsTemplate(
            title='モーションカメラ', text='動体検知してLINENotifyに通知します', actions=[
                PostbackTemplateAction(label='起動', data='起動'),
                PostbackTemplateAction(label='終了', data='終了'),
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'CPU温度':
        result = subprocess.check_output("vcgencmd measure_temp",shell=True)
        result = result.replace('temp=',"").replace("'C","").replace("\n","")
        message = "現在のラズパイのCPU温度は{}度です".format(result)
        main(message)
    elif text =='じゃんけん':
        buttons_template = ButtonsTemplate(
            title='じゃんけん', text='さいしょはグー、じゃんけん...', actions=[
                PostbackTemplateAction(label='ぐー', data='ぐー'),
                PostbackTemplateAction(label='ちょき', data='ちょき'),
                PostbackTemplateAction(label='ぱー', data='ぱー'),
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)


    elif text == 'カチューシャ':
        subprocess.check_call(['python','buzzer.py'])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='鳴りました'))

    elif text == "人感センサー":
        buttons_template = ButtonsTemplate(title='人感センサー', text='動体検知してここに通知します', actions=[
                 PostbackTemplateAction(label='起動', data='開始'),
                 PostbackTemplateAction(label='終了', data='終わり'),])
        template_message = TemplateSendMessage(alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text =="カメラ":
        message = "ただいま撮影中..."
        main(message)
        subprocess.check_call(['python','camera.py'])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='LINENotifyに写真を送ったよ!'))

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == '起動':
        subprocess.check_call(['sudo','motion'])
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='起動しました。'))
    elif event.postback.data == '終了':
        os.system('sudo service motion stop')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text ='終了しました'))

    elif event.postback.data == '開始':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='センサー起動'))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(25,GPIO.IN)
        time.sleep(2)
        while True:
            if(GPIO.input(25) == GPIO.HIGH):
                message = "人を感知しました"
                main(message)
                time.sleep(3)
                subprocess.check_call(['python','buzzer2.py'])
            else:
                pass


    elif event.postback.data == '終わり':
        GPIO.cleanup(25)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='終了します'))



    elif event.postback.data =='ぐー':
        gu = 0
        hands = ["グー", "チョキ", "パー"]
        judge = ["あいこ", "負け", "勝ち"]


        print("0:グー　1:チョキ　2:パー")
        message = ("あなたは" + hands[gu] + "をだしました")
        main(message)
        m = random.randint(0, 2)
        message = ("相手は" + hands[m] + "をだしました")
        main(message)

        i = (gu - m + 3) % 3
        main(judge[i])
 
    elif event.postback.data =='ちょき':
        tyoki = 1
        hands = ["グー", "チョキ", "パー"]
        judge = ["あいこ", "負け", "勝ち"]


        print("0:グー　1:チョキ　2:パー")
        message = ("あなたは" + hands[tyoki] + "をだしました")
        main(message)
        m = random.randint(0, 2)
        message = ("相手は" + hands[m] + "をだしました")
        main(message)

        i = (tyoki - m + 3) % 3
        main(judge[i])
 
    elif event.postback.data =='ぱー':
        pa = 2
        hands = ["グー", "チョキ", "パー"]
        judge = ["あいこ", "負け", "勝ち"]


        print("0:グー　1:チョキ　2:パー")
        message = ("あなたは" + hands[gu] + "をだしました")
        main(message)
        m = random.randint(0, 2)
        message = ("相手は" + hands[m] + "をだしました")
        main(message)

        i = (gu - m + 3) % 3
        main(judge[i])



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
 
    # create tmp dir for download content
    make_static_tmp_dir()
 
    app.run(debug=options.debug, port=options.port)
