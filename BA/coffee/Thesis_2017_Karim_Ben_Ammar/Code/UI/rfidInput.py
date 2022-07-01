#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import qrcode
import os
import time
import sys


def read():

    while True:
        try:
            temp1 = ""
            MIFAREReader = MFRC522.MFRC522()
            (status, TagType) = MIFAREReader.MFRC522_Request(
                MIFAREReader.PICC_REQIDL)
            (status, temp) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK and not os.path.isfile("/home/pi/CoffeeMachine/UI/androidOrder.txt") and not os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt") and not os.path.isfile("/home/pi/CoffeeMachine/UI/userUID.png") and not os.path.isfile("/home/pi/CoffeeMachine/UI/nowater.txt"):
                temp1 = hex(temp[0])[2:] + hex(temp[1])[2:] + \
                    hex(temp[2])[2:] + hex(temp[3])[2:]
            elif os.path.isfile("/home/pi/CoffeeMachine/UI/androidOrder.txt"):
                with open("/home/pi/CoffeeMachine/UI/androidOrder.txt") as f:
                    temp1 = f.readline()
                os.remove("/home/pi/CoffeeMachine/UI/androidOrder.txt")
            if not os.path.isfile('userUID.png') and temp1:
                with open("/home/pi/CoffeeMachine/UI/buzz.txt", "a") as f:
                    pass
                img = qrcode.make(temp1)
                img.save("/home/pi/CoffeeMachine/UI/userUID.png")
                with open("/home/pi/CoffeeMachine/UI/uid.txt", "a+") as f:
                    f.write(temp1)
            time.sleep(0.5)
        except:
            with open("/home/pi/logs/rfid.log", "a") as f:
                f.write("RFID error: %s" % sys.exc_info()[0])
            raise
        finally:
            GPIO.cleanup()

#!/usr/bin/env python
# -*- coding: utf8 -*-

# import RPi.GPIO as GPIO
# import MFRC522
# import signal
# import qrcode
# import os
# import time
# import sys
#
# def read(p):
#     uid = ""
#     reading = True
#     while reading:
#         try:
#             MIFAREReader = MFRC522.MFRC522()
#             (status, TagType) = MIFAREReader.MFRC522_Request(
#                 MIFAREReader.PICC_REQIDL)
#             (status, temp) = MIFAREReader.MFRC522_Anticoll()
#             if status == MIFAREReader.MI_OK and not os.path.isfile("/home/pi/CoffeeMachine/UI/androidOrder.txt") and not os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt"):
#                 uid = hex(temp[0])[2:] + hex(temp[1])[2:] + \
#                     hex(temp[2])[2:] + hex(temp[3])[2:]
#             elif os.path.isfile("/home/pi/CoffeeMachine/UI/androidOrder.txt"):
#                 with open("/home/pi/CoffeeMachine/UI/androidOrder.txt") as f:
#                     uid = f.readline()
#                 os.remove("/home/pi/CoffeeMachine/UI/androidOrder.txt")
#             if not os.path.isfile('userUID.png') and uid:
#                 #reading = False
#                 img = qrcode.make(uid)
#                 img.save("/home/pi/CoffeeMachine/UI/userUID.png")
#                 with open("/home/pi/CoffeeMachine/UI/uid.txt", "a+") as f:
#                     f.write(uid)
#                     f.close()
#             time.sleep(0.5)
#         except:
#             with open("/home/pi/logs/rfid.log", "a") as f:
#                 f.write("RFID error: %s \n" % sys.exc_info()[0])
#                 f.close()
#             raise
#         finally:
#             #p.send(uid)
#             GPIO.cleanup()
