import os
import RPi.GPIO as GPIO
import time
import atexit
import SharedArray as sa

import sys
#def exit_handler():
#     GPIO.cleanup()

def lockIt():

    lockPin = 37
    buzzerPin = 40
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(lockPin, GPIO.OUT)
    GPIO.setup(buzzerPin, GPIO.OUT)

    #try :
    #    flags = sa.attach("shm://coffeeMachine")
    #except:
    #    with open("/home/pi/logs/shm.log", "a") as f:
    #        f.write("SHM error: %s" % sys.exc_info()[0])
    #        f.close()
    #    raise
    buzz = False
    #PATH = "/home/pi/CoffeeMachine/UI/unlockPipe"
    while True:
        if os.path.isfile("/home/pi/CoffeeMachine/UI/unlock.txt"):
        # try:
        #     pipe = os.open(PATH, os.O_RDONLY | os.O_NONBLOCK);
        #     input = os.read(pipe,bufferSize);
        # except OSError as err:
        #     if err.errno == 11:
        #         continue;
        #     else:
        #         with open("/home/pi/logs/unlockFiFo.log", "a") as f:
        #             f.write(err)
        #             f.flush()
        #         raise err;
        #if flags[0] == 1:
            GPIO.output(lockPin, 1)
        else :
            GPIO.output(lockPin, 0)
        if os.path.isfile("/home/pi/CoffeeMachine/UI/buzz.txt") and buzz:
            GPIO.output(buzzerPin, 0)
            buzz = False
            os.remove("/home/pi/CoffeeMachine/UI/buzz.txt")
        elif os.path.isfile("/home/pi/CoffeeMachine/UI/buzz.txt") and not buzz:
            buzz = True
            GPIO.output(buzzerPin, 1)
        time.sleep(0.5)
    atexit.register(GPIO.cleanup())
