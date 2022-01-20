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
mery_merody=[ra,si,do,ra,do,do,si,ra,si,mi,si,do,587,si,587,587,do,si,ra ,659,880,784,880,784,698,698,659,587,659,ra,698,587,659,do,587,587,do,si,440,659,880,784,880,784,698,698,659,587,659,ra,698,587,659,do,587,587,do,si,440]
mery_rhythm=[0.6,0.2,0.5,0.2,0.2,0.2,0.2,0.3,0.4,0.5,0.6,0.3,0.5,0.3,0.2,0.2,0.2,0.2,0.8,0.5,0.5,0.5,0.2,0.3,0.2,0.2,0.2,0.2,0.5,0.5,0.4,0.3,0.5,0.2,0.2,0.2,0.2,0.2,0.5,0.5,0.5,0.5,0.2,0.3,0.2,0.2,0.2,0.2,0.5,0.5,0.4,0.3,0.5,0.2,0.2,0.2,0.2,0.2,0.5]
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.OUT,initial=GPIO.LOW)
print(len(mery_merody))
print(len(mery_rhythm))
p = GPIO.PWM(pin,1)
p.start(50)
p.ChangeFrequency(2)
time.sleep(2)

for i, oto in enumerate(mery_merody):
    p.start(50)
    p.ChangeFrequency(oto)
    time.sleep(mery_rhythm[i])
    p.stop()
    time.sleep(0.03)

p.stop()
GPIO.cleanup()
