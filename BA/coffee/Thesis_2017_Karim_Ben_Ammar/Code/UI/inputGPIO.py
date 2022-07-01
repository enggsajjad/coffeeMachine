import os
import RPi.GPIO as GPIO
import time
import datetime
import atexit

from rfidInput import read

#from server import tornadoServer
from unlockMachine import lockIt
import multiprocessing

from stateMachine import CoffeeMachine
from transitions.core import MachineError

GPIO.setmode(GPIO.BOARD)

fileName = ''
start = datetime.time(0, 0, 0)
end = datetime.time(0, 0, 0)
days = 7

lastLog = ''
currentOrder = ""
waterCounter = 0
idleCount = 0
previousWaterFLow2 = 1
previousWaterFLow1 = 1
previousGrinder = 1

grinderPin = 33
waterFlow1Pin = 29
waterFlow2Pin = 31
waterLevelPin = 35

#coffeeMachine = CoffeeMachine()

def makeSpace():
    dir_to_search = "/home/pi/CoffeeMachine/UI/logs"
    for dirpath, dirnames, filenames in os.walk(dir_to_search):
        for file in filenames:
            curpath = os.path.join(dirpath, file)
            file_modified = datetime.datetime.fromtimestamp(
                os.path.getmtime(curpath))
            if datetime.datetime.now() - file_modified > datetime.timedelta(hours=days * 24):
                os.remove(curpath)


def checkIfMidnight():
    timestamp = datetime.datetime.now().time()
    if start <= timestamp and timestamp <= end:
        global fileName
        temp = time.strftime("%Y-%m-%d", time.gmtime())
        if not temp == fileName:
            fileName = temp
        global lastLog
        lastLog = ''

def parseSensors(line):
    d = {}
    d["name"] = line.split(":")[0]
    d["pins"] = [sensor(i) for i in line.split(":")[1].split(";")]
    return d

def sensor(sen):
    sensor = {}
    sensor['pin'] = int(sen.split(",")[0])
    sensor['type'] = 1 if sen.split(",")[1].strip() == 'IN' else 0
    GPIO.setup(sensor['pin'], sensor['type'], pull_up_down=GPIO.PUD_UP)
    return sensor

def preprocessing(content):
    array = []
    for line in content:
        array.append(parseSensors(line))
    return array

def writeToFile(log):
    #checkIfMidnight()
    #global fileName
    logName = time.strftime("%Y-%m-%d", time.gmtime())
    with open("/home/pi/CoffeeMachine/UI/logs/" + logName + ".txt", "a+") as f:
        f.write(log)
        f.flush()

def printLog(array):
    timeStamp = "%s [" % time.strftime("%H:%M:%S", time.localtime())

    s = ''
    for sensor in array:

        s += "%s" % (''.join(["%s," % (GPIO.input(x['pin']) if x['type']
                                       == 1 else GPIO.output(x['pin'])) for x in sensor['pins']]))
    s = s[:-1]

    # global coffeeMachine
    #
    # try:
    #     moveToState = getattr(coffeeMachine, coffeeMachine.convertToFunc(s))
    #     moveToState()
    # except AttributeError as e:
    #     print(str(e))
    #     pass
    # except MachineError :
    #     coffeeMachine.toUnkown()
    #     print(" Input :%s." %s)
    #     pass

    global lastLog
    global currentOrder
    global waterCounter
    global previousWaterFLow2
    global previousWaterFLow1
    global grinderPin
    global waterFlow1Pin
    global waterFlow2Pin
    global waterLevelPin
    global idleCount
    if GPIO.input(waterFlow1Pin) == previousWaterFLow1 and GPIO.input(waterFlow2Pin) == previousWaterFLow2 and GPIO.input(grinderPin) == 1:
            if GPIO.input(waterLevelPin) == 1 and not os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt"):
                with open("/home/pi/CoffeeMachine/UI/nowater.txt", "a") as f:
                    pass
            elif GPIO.input(waterLevelPin) == 0 and os.path.isfile("/home/pi/CoffeeMachine/UI/nowater.txt"):
                os.remove("/home/pi/CoffeeMachine/UI/nowater.txt")

            if idleCount < 6000 and not currentOrder == '':
                idleCount = idleCount + 1
            elif idleCount >= 6000:
                idleCount = 0
                currentOrder = ''
                waterCounter = 0
                with open("/home/pi/CoffeeMachine/UI/stop.txt", "a") as f:
                    pass
                with open("/home/pi/CoffeeMachine/UI/done.txt", "a") as f:
                    pass
                if os.path.isfile("/home/pi/CoffeeMachine/UI/unlock.txt"):
                   os.remove("/home/pi/CoffeeMachine/UI/unlock.txt")

    if not os.path.isfile("/home/pi/CoffeeMachine/UI/maintenance.txt"):
        global previousGrinder
        if GPIO.input(grinderPin) == 0 and previousGrinder == 1 and not currentOrder == 'coffee':
            if os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt") :
                with open("/home/pi/CoffeeMachine/UI/order.txt", "r") as j:
                    temp = j.readline()
                if temp == "water\n":
                    os.remove("/home/pi/CoffeeMachine/UI/order.txt")
            with open("/home/pi/CoffeeMachine/UI/order.txt", "a+") as f:
                f.write("coffee\n")
                f.close()
            with open("/home/pi/CoffeeMachine/UI/stop.txt", "a") as f:
                pass
            currentOrder = 'coffee'
            previousGrinder = 1
        elif GPIO.input(grinderPin) == 1 and previousGrinder == 0:
            previousGrinder = 1
        elif not (GPIO.input(waterFlow1Pin) == previousWaterFLow1) or not (GPIO.input(waterFlow2Pin) == previousWaterFLow2):
            previousWaterFLow2 = GPIO.input(waterFlow2Pin)
            previousWaterFLow1 = GPIO.input(waterFlow1Pin)
            idleCount = 0
            if not os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt"):
                with open("/home/pi/CoffeeMachine/UI/order.txt", "a+") as f:
                    f.write("water\n")
                currentOrder = 'water'
            elif not os.path.isfile("/home/pi/CoffeeMachine/UI/unlock.txt") and os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt") and currentOrder == 'water':
                with open("/home/pi/CoffeeMachine/UI/unlock.txt", "a") as f:
                    pass

    if not (s == lastLog):
        lastLog = s
        s = timeStamp + s + "]\n"
        writeToFile(s)


def main():

    #p = multiprocessing.Process(target=tornadoServer)
    #p.daemon = True
    #p.start()
    makeSpace()
    p1 = multiprocessing.Process(target=lockIt)
    p1.daemon = True
    p1.start()

    p2 = multiprocessing.Process(target=read)
    p2.daemon = True
    p2.start()

    configFile = "/home/pi/CoffeeMachine/UI/config.txt"
    with open(configFile) as f:
        content = f.readlines()

    global fileName
    fileName = time.strftime("%Y-%m-%d", time.gmtime())

    array = preprocessing(content)
    temp = "[%s" % (''.join([x['name'] + ', ' for x in array]))
    temp = temp[:-1] + ']\n'
    writeToFile(temp)

    global previousWaterFLow2
    previousWaterFLow2 = GPIO.input(waterFlow2Pin)

    global previousWaterFLow1
    previousWaterFLow1 = GPIO.input(waterFlow1Pin)

    while True:
        printLog(array)
        time.sleep(0.001)

def exit_app():
    GPIO.cleanup()

if __name__ == "__main__":
    main()
    atexit.register(exit_app)
