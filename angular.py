import numpy as np
import time 
import RPi.GPIO as GPIO
import os 
import pygame


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pygame.mixer.init()

def reading():

    TRIG = 27
    ECHO = 17
    

    GPIO.setup(TRIG,GPIO.OUT)
  
    GPIO.setup(ECHO,GPIO.IN)
    time.sleep(0.3)


    GPIO.output(TRIG, True)
    print("pulse sent")
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        signaloff = time.time()

    while GPIO.input(ECHO) == 1:
        signalon = time.time()

    timepassed = signalon - signaloff
    print("echo recieved")

    #speed in cm/s
    speed = 34300
    #need factor two for there and back
    distance = round((speed*timepassed)/2,2)
    
    return distance
    
def angular_reading():
    m = np.linspace(1,2,10)
    rec = []
    for i in m :
        d = reading()
        print(d)
        time.sleep(2)
        if d <= 40:
            rec.append(d)
    print(rec)
    print(int(len(rec)))
    
    return 

angular_reading()
        
        
    


