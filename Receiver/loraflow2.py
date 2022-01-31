#!/usr/bin/env python3
import os
import errno
from time import gmtime, strftime
import time
from threading import Thread
from DBHandler import DBHandler
import json
import string
import serial
import RPi.GPIO as GPIO
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
    
FIFO = '/tmp/loraflow'



ser = serial.Serial(
 #port='/dev/ttyS0', #might be  port='/dev/ttyAMA0' as well
 port='/dev/ttyAMA0',
 baudrate = 9600,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)


#RPi pins
M0 = 23
M1 = 24


# global variables
pipeMsg = "";



def set_lora_module_normal_mode():
    GPIO.setmode(GPIO.BCM)
    #set lora module to normal mode
    GPIO.setup(M0,GPIO.OUT)
    GPIO.setup(M1,GPIO.OUT)

    GPIO.output(M0,GPIO.LOW)
    GPIO.output(M1,GPIO.LOW)
    


def send_lora_msg( msg ):
    print(msg)
    
    
def serial_thread(threadname):
    global pipeMsg
    global lastValidSerialMsg
    global ws
    
    while True:
        
        #SERIAL READ
        
        data = ser.readline()
        serialMsg = data.decode('ascii','ignore')
        
        if serialMsg != "" :
            
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " " + 'Got lora msg: "{0}"'.format(serialMsg))
            #  "temperature=23.06:moisture=16;"
            first = 0
            separator = 0
            temp = ""
            i = 0 
            try:
                list = serialMsg.split(':')
                temp = list[0].split('=')[1]
                soil = list[1].split('=')[1]
                soil = soil.replace(";","")
            except:
                print ("Conversion error")
                return
            write_database(soil,temp)
            print ("DB Successfully written")
        


def write_database(soil,temp):
    d = DBHandler()
    d.Write(soil,temp)
    d.Disconnect()
    
#SOCKET RELATED

thread2 = Thread( target=serial_thread, args=("Serial Thread", ) )
thread2.start()

thread2.join()

