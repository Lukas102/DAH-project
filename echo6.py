"""
Created on Tue Oct 29 15:06:35 2024

@author: s2025922
"""
import numpy as np
import time 
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
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
# we're no longer using the GPIO, so tell software we're done
    GPIO.cleanup()
#dist = float(reading())
#print(f"the distance is {dist:.2f} cm" )

def sensor():
    lights = [10,9,11,5]
    for LED in lights:
        GPIO.setup(LED, GPIO.OUT)
        GPIO.output(LED, GPIO.LOW)
        
    while True:
        d = reading()
        print(d)
    
        if 150 < int(d) <= 200 :
            GPIO.output(lights[0], GPIO.HIGH)
            
            for LED in lights[1:-1] : 
                GPIO.output(LED, GPIO.LOW) 
                
            print("d is 150-200")
        
        elif  100 < int(d) <= 150:
            
            for LED in lights[0:1] : 
                GPIO.output(LED, GPIO.HIGH) 
                
            for LED in lights[2:-1] : 
                GPIO.output(LED, GPIO.LOW) 
            
            print("d is 100-150")
                
        elif 50  < int(d) <= 100:
            for LED in lights[0:2] : 
                GPIO.output(LED, GPIO.HIGH) 
    
            GPIO.output(lights[3], GPIO.LOW) 
                
        elif 25  < int(d) <= 50:
            print("d is 25-50")
            for LED in lights: 
                GPIO.output(LED, GPIO.HIGH) 
                
        elif 0 <= int(d) <= 25:
            print("d is 0-25")
            
            for LED in lights:
                GPIO.output(LED, GPIO.HIGH)

                   
            time.sleep(0.01*float(d))
            
            for LED in lights:
                GPIO.output(LED, GPIO.LOW)

                
            time.sleep(0.01*float(d))
                
        
        else:
            for LED in lights:
                GPIO.output(LED, GPIO.LOW)
                
        
        
    
        
        
        
    return
    
sensor()
#print(f"{sensor()}")
