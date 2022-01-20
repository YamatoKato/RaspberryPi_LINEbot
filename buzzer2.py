#coding:utf-8

import RPi.GPIO as GPIO
import time

pin = 27

do = 523
re = 294
mi = 330
fa = 349
so = 392
ra = 440
si = 494
#カチューシャ
mery_merody=[si,so,si,so]
mery_rhythm=[0.2,0.2,0.2,0.2]
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.OUT,initial=GPIO.LOW)
print(len(mery_merody))
print(len(mery_rhythm))
p = GPIO.PWM(pin,1)
p.start(50)
p.ChangeFrequency(2)

for i, oto in enumerate(mery_merody):
    p.start(50)
    p.ChangeFrequency(oto)
    time.sleep(mery_rhythm[i])
    p.stop()
    time.sleep(0.03)
p.stop()
GPIO.cleanup(27)
