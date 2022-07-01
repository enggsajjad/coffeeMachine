import os
import RPi.GPIO as GPIO
import time

def buzz():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT)
    try :
        steps = 2
        while steps > 0 :
            GPIO.output(40, 1)
            time.sleep(0.3)
            GPIO.output(40, 0)
            steps = steps - 1
            time.sleep(0.3)
    except :
        pass
    finally :
        GPIO.cleanup()
