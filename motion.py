#!/usr/bin/env python

import sys
import RPi.GPIO as GPIO
import time
import telepot
import datetime
import telegram
import picamera
import os.path

if (len(sys.argv) < 3):
   print( "Usage:" +  sys.argv[0] + " chat_id day/night")
   sys.exit(1)

GPIO.setmode(GPIO.BCM)
PIR_PIN=7
GPIO.setup(PIR_PIN,GPIO.IN)

chatid=int(str(sys.argv[1]))
day_night=str(sys.argv[2])

home_dir='/home/pi/Jarvis/JarvisMobile'
stop_file=home_dir + '/STOP.MOTION'

os.remove(stop_file)

botKey = ""

with open(home_dir + '/cfg/bot.cfg','r') as bot_cfg_file:
        for line in bot_cfg_file:
                botKey = line.strip()
		
botMotion = telegram.Bot(token=botKey)

def sendSnap():
        #Get the photo
        camera = picamera.PiCamera()
        timeStamp = time.strftime("%Y%m%d_%H%M%S")
        filename = home_dir + "/captures/"+timeStamp+"_Capture.jpg"
        camera.capture(filename)
        print("Photo taken")
        camera.close()

        # Sends a message to the chat
        botMotion.sendPhoto(chat_id=chatid, photo=open(filename, 'rb'))
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
        botMotion.sendPhoto(chat_id=chatid, photo=open(filename, 'rb'))
        print("Photo sent")

try:
    print "PIR Module Test (CTRL+C to exit)"
    time.sleep(6)
    print "Ready"
    botMotion.sendMessage(chatid , 'Motion sensor running.')


    while True:
            if GPIO.input(PIR_PIN):
                print "Motion Detected!"
                if day_night == "day":
		   sendSnap()
		elif day_night == "night":
		   sendNightPic()
            time.sleep(1)
	    if os.path.isfile(stop_file):
		print("Stop file found. Shutting down motion detection.") 
		break 
            
except KeyboardInterrupt:
        print "Quit"
        GPIO.cleanup()
