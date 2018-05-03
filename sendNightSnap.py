#!/usr/bin/env python

import sys
import time
import datetime
import telegram
import picamera

home_dir='/home/pi/Jarvis/JarvisHomeMonitoring'

botKey = ""

with open(home_dir + '/cfg/bot.cfg','r') as bot_cfg_file:
        for line in bot_cfg_file:
                botKey = line.strip()

chat_id=int(str(sys.argv[1]))
# Connect to our bot
bot = telegram.Bot(token=botKey)


#Get the photo
with picamera.PiCamera() as camera:
        camera.resolution = ( 1280,960 )
        camera.exposure_mode = 'night'
        camera.framerate =1
        camera.shutter_speed = 6000000
        camera.iso = 1600
        timeStamp=time.strftime("%Y%m%d_%H%M%S")
        filename=home_dir + "/captures/"+timeStamp+"_NightCapture.jpg"
        camera.capture(filename)
        print("Photo taken")
        camera.close()

# Sends a message to the chat
bot.sendPhoto(chat_id=chat_id, photo=open(filename, 'rb'))
print("Photo sent")
