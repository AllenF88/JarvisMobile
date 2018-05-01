#!/usr/bin/env python

import sys
import time
import datetime
import telegram
import picamera

botKey = ""

with open('/home/pi/JarvisMobile/cfg/bot.cfg','r') as bot_cfg_file:
	for line in bot_cfg_file:
		botKey = line.strip()
    print (botKey)

chat_id=int(str(sys.argv[1]))
print("script called, with " + str(chat_id))
# Connect to our bot
bot = telegram.Bot(token=botKey)
#Get the photo
camera=picamera.PiCamera()
timeStamp=time.strftime("%Y%m%d_%H%M%S")
filename="/home/pi/JarvisMobile/captures/"+timeStamp+"_Capture.jpg"
camera.capture(filename)
print("Photo taken")
camera.close()
bot.sendPhoto(chat_id=chat_id, photo=open(filename, 'rb'))
print("Photo sent")
