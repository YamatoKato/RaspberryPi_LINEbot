#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import requests

url = "https://notify-api.line.me/api/notify"
access_token = '自身のLINotifyのトークン'
headers = {'Authorization': 'Bearer ' + access_token}

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25,GPIO.IN)
    time.sleep(2)

    while True:
        if(GPIO.input(25) == GPIO.HIGH):
            print("感知しました")
            time.sleep(10)
            #メッセージを送信
            message = '人を感知しました'
            payload = {'message': message}
            r = requests.post(url, headers=headers, params=payload,)
        else:
            pass

except KeyboardInterrupt:
    print("中断中...")
finally:
    GPIO.cleanup()
    print("GPIOclean")
