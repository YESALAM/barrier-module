#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

import requests
import json

import time
import sys

#change this id based on what is going to be
b_id  = 1

try:
    arguments = sys.argv
    count = len(arguments)
    if count==2:
        b_id = arguments[1]
except:
    print "argument error"

def verify(uid):
    base_url = "http://ec2-52-90-129-59.compute-1.amazonaws.com:5000"
    final_url = base_url + "/fetch"

    payload  = {'b_id':b_id,'uuid':uid}
    print "sending to server",final_url
    response = requests.post(final_url, data=payload)

    json_response = response.text
    print "response is",json_response
    js = json.loads(json_response)
    result = js['result']
    return result

def continous_redLight():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    print "Red LED on"


def redLight():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    print "LED on"
    GPIO.output(23, GPIO.HIGH)
    time.sleep(5)
    print "LED off"
    GPIO.output(23, GPIO.LOW)

def greeLight():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    print "LED on"
    GPIO.output(18, GPIO.HIGH)
    time.sleep(5)
    print "LED off"
    GPIO.output(18, GPIO.LOW)

def redLightFlash():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    print "LED on"
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)
    time.sleep(1)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)
    time.sleep(1)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)
    time.sleep(1)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)
    time.sleep(1)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23, GPIO.LOW)

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

continous_redLight()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        #status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        #if status == MIFAREReader.MI_OK:
        #    MIFAREReader.MFRC522_Read(8)
        #    MIFAREReader.MFRC522_StopCrypto1()
        suid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
        result = verify(suid)
        if result == 'ok':
            print 'Ok to go'
            greeLight()
        else:
            print 'Can not go'
            redLightFlash()
        #else:
        #    print "Authentication error"
        #    redLightFlash()

