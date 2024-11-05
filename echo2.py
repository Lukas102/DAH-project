# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:06:35 2024

@author: s2025922
"""
import numpy as np
import RPi.GPIO as GPIO
import time

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
  
#defintion to turn LEDs on in diff patterns as distance to object changes
def light(distance_l):
    #need to change all pins assigned, maybe port to a bus if wires get too
    #much
    LED0 = 10
    LED01 = 9
    LED02 = 11
    LED03 = 5
    
    lights = [10,9,11,5]
    
    GPIO.setup(LED0, GPIO.OUT)
    GPIO.setup(LED01, GPIO.OUT)
    GPIO.setup(LED02, GPIO.OUT)
    GPIO.setup(LED03, GPIO.OUT)

    sensor()
    
    if 150 < distance_l[-1] <= 200 :
        GPIO.output(LED0, GPIO.HIGH)
        
        for LED in lights[1:-1] : 
            GPIO.output(LED, GPIO.LOW) 
        
    elif  100 < distance_l[-1]  <= 150:
        GPIO.output(LED01, GPIO.HIGH)
        
       # for LED in lights[1:-1]: 
            #GPIO.output(LED, GPIO.LOW)
            
    elif 50  < distance_l[-1]  <= 100:
        GPIO.output(LED02, GPIO.HIGH)
        
       # for LED in lights[2:-1]: 
            #GPIO.output(LED, GPIO.LOW)
        
    elif 25  < distance_l[-1]  <= 50:
        GPIO.output(LED03, GPIO.HIGH)
        
        GPIO.output(LED03.LOW)
     
    #flashing lights
    elif 0 <= distance_l[-1] <= 25:
        while True:
            for LED in lights:
                GPIO.output(LED, GPIO.LOW)

            time.sleep(0.01*int(distance_l[-1]))
            
            for LED in lights:
                GPIO.output(LED, GPIO.HIGH)
                
            time.sleep(0.01*int(distance_l[-1]))
            
            
    else:
        for LED in lights:
            GPIO.output(LED, GPIO.LOW)
            
    return
        
        

    
    
    
#print("the distance is " + str(reading()) + "cm" )