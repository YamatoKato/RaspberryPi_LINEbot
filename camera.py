#!/usr/bin/env python
# -*- coding: utf-8 -*-
from picamera import PiCamera
from time import sleep
import datetime
import requests
import sys
import datetime
 
camera = PiCamera()
now = datetime.datetime.now()
camera.capture("/home/pi/Pictures/{0:%Y-%m-%d_%H%M%S}.jpg".format(now))
fname = "/home/pi/Pictures/{0:%Y-%m-%d_%H%M%S}.jpg".format(now)
camera.resolution = (1980, 1080)
# 最大2592*1944
camera.start_preview()
# ディスプレイを繋いでいる時のみプレビュー
camera.annotate_text = "RaspberryPi"
# 画像にテキストを追加する
camera.annotate_text_size = 100
# テキストサイズ6〜160 デフォルトは32
camera.brightness = 50
# 明るさ設定0〜100 デフォルトは50
camera.contrast = 50
# コントラスト設定0〜100 デフォルトは50
camera.image_effect = 'none'
# 画像エフェクト
camera.color_effects = None
# カラーエフェクト
camera.awb_mode = 'auto'
# オートホワイトバランス
camera.sharpness = 0
# シャープネス デフォルトは0
camera.saturation = 0
# 彩度 デフォルトは0
camera.ISO = 0
# ISO デフォルトは0
camera.exposure_compensation = 0
# 露出補正 デフォルトは0
camera.exposure_mode = 'auto'
# 露出モード デフォルトはauto
camera.meter_mode = 'average'
# メーターモード？ デフォルトはaverage
camera.rotation = 0
# 画像の回転
camera.hflip = False
# 水平反転
camera.vflip = False
# 垂直反転
camera.crop = (0.0, 0.0, 1.0, 1.0)
# ？
sleep(3)
camera.stop_preview()
 
# ここからLINE送信用
 
def main():
    url = 'https://notify-api.line.me/api/notify'
    token = '自身のLINENotifyのトークン'
    headers = {'Authorization' : 'Bearer '+token}
    message = datetime.datetime.now()
    message = message - datetime.timedelta(hours=16)
    payload = {'message' : message}
    files = {"imageFile": open(fname, "rb")}
    r = requests.post(url, headers=headers, data=payload, files=files,)
    print(r)
 
if __name__ == '__main__':
    main()
