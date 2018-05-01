#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import telepot
import datetime
import telegram
import picamera

GPIO.setmode(GPIO.BCM)
PIR_PIN=7
GPIO.setup(PIR_PIN,GPIO.IN)
chat_id=330392544
botKey = ""

with open('/home/pi/JarvisMobile/cfg/bot.cfg','r') as bot_cfg_file:
	for line in bot_cfg_file:
		botKey = line.strip()
    print (botKey)

def sendSnap():
        # Connect to our bot
        botMotion = telegram.Bot(token=botKey)
        #Get the photo
        camera=picamera.PiCamera()
        timeStamp=time.strftime("%Y%m%d_%H%M%S")
        filename="/home/pi/JarvisMobile/captures/"+timeStamp+"_Capture.jpg"
        camera.capture(filename)
        print("Photo taken")
        camera.close()
        # Sends a message to the chat
        botMotion.sendPhoto(chat_id=chat_id, photo=open(filename, 'rb'))
        print("Photo sent")

try:
    print "PIR Module Test (CTRL+C to exit)"
    time.sleep(6)
    print "Ready"

    while True:
            if GPIO.input(PIR_PIN):
                print "Motion Detected!"
		sendSnap()
            time.sleep(1)
            
except KeyboardInterrupt:
        print "Quit"
        GPIO.cleanup()