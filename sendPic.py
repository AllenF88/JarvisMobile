#!/usr/bin/env python

import sys
import time
import datetime
import telegram
import picamera


if (len(sys.argv) < 3):
   print( "Usage:" +  sys.argv[0] + " chatid PicMode")
   sys.exit(1)

home_dir='/home/pi/Jarvis/JarvisMobile'

botKey = ""

with open(home_dir + '/cfg/bot.cfg','r') as bot_cfg_file:
        for line in bot_cfg_file:
                botKey = line.strip()

botMiniMe = telegram.Bot(token=botKey)

chatid=int(str(sys.argv[1]))
mode=str(sys.argv[2])

print("script called, with " + str(chatid))
botMiniMe.sendMessage(chatid,'MiniMe here, taking the pic.')

def sendSnap():
        #Get the photo
        camera = picamera.PiCamera()
        timeStamp = time.strftime("%Y%m%d_%H%M%S")
        filename = home_dir + "/captures/"+timeStamp+"_Capture.jpg"
        camera.capture(filename)
        print("Photo taken")
        camera.close()

        # Sends a message to the chat
        botMiniMe.sendPhoto(chat_id=chatid, photo=open(filename, 'rb'))
        print("Photo sent")

def sendNightPic():
	# Connect to our bot
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
        botMiniMe.sendPhoto(chat_id=chatid, photo=open(filename, 'rb'))
        print("Photo sent")
   
#Start of script here

if mode == "Day":
	sendSnap()
elif mode == "Night":
	sendNightPic()        
