# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:06:35 2024

@author: s2025922
"""
import numpy as np
import RPi.GPIO as GPIO
import time
import os

def reading():
# remember to change the GPIO values below to match your sensors
# GPIO output = the pin that's connected to "Trig" on the sensor
# GPIO input = the pin that's connected to "Echo" on the sensor
    TRIG = 11
    ECHO = 13

    # Disable any warning message such as GPIO pins in use
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    # Setup the GPIO pins for TRIG and ECHO, including defining
    #trigger as an ouput
    GPIO.setup(TRIG,GPIO.OUT)
    #echo as an input
    GPIO.setup(ECHO,GPIO.IN)
    #ensuring initial trigger ouput is set low
    GPIO.output(TRIG, False)
    print("output set low")
    time.sleep(1)
# sensor manual says a pulse length of 10Us will trigger the
# sensor to transmit 8 cycles of ultrasonic burst at 40kHz and
# wait for the reflected ultrasonic burst to be received
# to get a pulse length of 10Us we need to start the pulse, then
# wait for 10 microseconds, then stop the pulse. This will
# result in the pulse length being 10Us.
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
# listen to the input pin. 0 means nothing is happening. Once a
# signal is received the value will be 1 so the while loop
# stops and has the last recorded time the signal was 0
    while GPIO.input(ECHO) == 0:
        signaloff = time.time()
# listen to the input pin. Once a signal is received, record the
# time the signal came through
    while GPIO.input(ECHO) == 1:
        signalon = time.time()
# work out the difference in the two recorded times above to
# calculate the distance of an object in front of the sensor
    timepassed = signalon - signaloff

    #speed in cm/s
    speed = 34300
    #need factor two for there and back
    distance = round((speed*timepassed)/2,2)
    
    return distance
# we're no longer using the GPIO, so tell software we're done
    GPIO.cleanup()
    
def sensor(distance):
    distance_l = []
    t = 60
    time_span = np.linspace(0,t,60)
    for i in time_span:
        print("the distance is " + str(reading()) + "cm" )
        distance.append(distance_l)
        
    return distance_l
  
#defintion to turn LEDs on in diff patterns as distance to object changes
def alarm():
    #putting pins in list then distributing
    
    lights = [10,9,11,5]
    for LED in lights:
        GPIO.setup(LED, GPIO.OUT)
    #setting all pins low to start    
    for LED in lights:
        GPIO.output(lights[0], GPIO.LOW)
        
    

    #running a loop which takes readings every second for 60 seconds from reading()
    t = np.linspace(0,60,60)
    for i in t:
        distance = reading()
        print("the distance is " + str(reading()) + "cm" )
     #setting first light on then second then third then fourth
        if 150 < distance <= 200 :
            GPIO.output(lights[0], GPIO.HIGH)
            print("d is 150-200")
             
            for LED in lights[1:-1] : 
                GPIO.output(LED, GPIO.LOW) 
                
        
        elif  100 < distance  <= 150:
            
            GPIO.output(lights[1], GPIO.HIGH)
            print("d is 100-150")
        
            for LED in lights[1:-1]: 
                GPIO.output(LED, GPIO.LOW)
            
        elif 50  < distance <= 100:
            GPIO.output(lights[2], GPIO.HIGH)
            print("d is 100-50")
            
            for LED in lights[2:-1]: 
                    GPIO.output(LED, GPIO.LOW)
        
        elif 25  < distance <= 50:
            print("d is 25-50")
            GPIO.output(lights[3], GPIO.HIGH)
            
            for LED in lights[2:-1]: 
                    GPIO.output(LED, GPIO.LOW)
     
        #flashing lights
        elif 0 <= distance <= 25:
            print("d is 150-200")
            
            for LED in lights:
                GPIO.output(LED, GPIO.HIGH)

                   
            time.sleep(0.01*float(distance))
            
            for LED in lights:
                GPIO.output(LED, GPIO.LOW)

                
            time.sleep(0.01*float(distance))
                
                
            
            
        else:
            for LED in lights:
                GPIO.output(LED, GPIO.LOW)
                
        time.sleep(1)
            
    return
        
        

   
alarm()
GPIO.cleanup()