import sys
from os import walk, path, remove
from multiprocessing import Process, Pipe

from transitions import Machine, core
from util import internet_on
from serverCommunication import passOrder
from dbHandler import addOfflineTransaction
from rfidInput import read
from buzzer import buzz


class CoffeeMachine(object):

    def convertToFunc(self, var):
        var.replace(" ", "")
        temp = var
        temp = temp.replace('0', 'A')
        temp = temp.replace('1', 'B')
        temp = temp.replace(',', 'C')
        return temp

    def __init__(self):
        transitions = []
        states = ['unkown', 'idle', 'noWater', 'unlocked']
        idleState = '0,1,1,1'
        noWaterState = '1,1,1,1'
        idleTrigger = self.convertToFunc(idleState)
        noWaterTrigger = self.convertToFunc(noWaterState)
        self.order = ''
        self.repeatedIdle = 0

        for (dirpath, dirnames, filenames) in walk("/home/pi/CoffeeMachine/UI/states"):
            for file in filenames:
                curpath = path.join(dirpath, file)
                file = file.split('.')[0]
                if file.isalpha():
                    states.append(file)
                    with open(curpath, "r+") as f:
                        temp = f.readlines()

                    wasIdle = True
                    for line in temp:
                        line = line.replace("\n", "")
                        trigger = self.convertToFunc(line)
                        if not line == idleState:
                            if wasIdle:
                                wasIdle = False
                                transitions.append(
                                    {'trigger': trigger, 'source': 'unlocked', 'dest': file, 'after': 'order_detected'})
                            else:
                                transitions.append(
                                    {'trigger': trigger, 'source': file, 'dest': file, 'after': 'resetIdleCounter'})
                        else:
                            wasIdle = True
                    transitions.append(
                        {'trigger': idleTrigger, 'source': file, 'dest': 'idle', 'before': 'order_ready'})
        transitions.append(
            {'trigger': noWaterTrigger, 'source': 'idle', 'dest': 'noWater', 'after': 'noWaterHandler'})
        transitions.append(
            {'trigger': idleTrigger, 'source': 'noWater', 'dest': 'idle', 'after': 'isWaterHandler'})
        transitions.append(
            {'trigger': idleTrigger, 'source': 'idle', 'dest': 'idle', 'after': 'repeated_idle'})
        transitions.append({'trigger': 'toUnkown', 'source': '*',
                            'dest': 'unkown', 'before': 'unkownHandler'})
        transitions.append(
            {'trigger': idleTrigger, 'source': 'unkown', 'dest': 'idle', 'after': 'backToIdle'})
        transitions.append({'trigger': 'unlockMachine', 'source': 'idle', 'dest': 'unlocked', 'before': 'unlock_machine'})
        transitions.append({'trigger': 'toIdle', 'source': '*', 'dest': 'idle'})
        self.machine = Machine(
            model=self, states=states, transitions=transitions, initial='idle')

    def resetIdleCounter(self):
        if self.repeatedIdle > 0:
            self.repeatedIdle = 0

    def order_ready(self):
        if self.order == '':
            with open("/home/pi/logs/orderReady.txt", "w") as f :
                f.write(self.state)
            self.order = self.state

    def unlock_machine(self):
        print("machine unlocked")
        with open("/home/pi/CoffeeMachine/UI/unlock.txt", "a") as f:
            pass

    def unkownHandler(self):
        print("This is an unkown state")
        #self.toIdle()


    def backToIdle(self):
        print("Back to idle state")

    def noWaterHandler(self):
        with open("/home/pi/CoffeeMachine/UI/nowater.txt", "a") as f:
            pass

    def isWaterHandler(self):
        remove("/home/pi/CoffeeMachine/UI/nowater.txt")

    def repeated_idle(self):
        if not self.order == '' and self.repeatedIdle < 1000:
            self.repeatedIdle = self.repeatedIdle + 1
        elif not self.order == '' and self.repeatedIdle >= 1000:
            os.remove("/home/pi/CoffeeMachine/UI/unlock.txt")
            with open("/home/pi/CoffeeMachine/UI/stop.txt", "a") as f:
                pass
            with open("/home/pi/CoffeeMachine/UI/order.txt", "w+") as f:
                f.write(self.order)
            if path.isfile("/home/pi/CoffeeMachine/UI/withMilk.txt"):
                black = "false"
            if self.order == 'water':
                water = "true"
            else:
                water = "false"
            if internet_on():
                try:
                    p = Process(target=passOrder, args=(self.uid, black, water))
                    p.start()
                except:
                    with open("/home/pi/logs/order.log", "a") as f:
                        f.write("Order error: %s \n" % sys.exc_info()[0])
                        f.close()
                    raise
            else:
                addOfflineTransaction(uid, black, water)
            self.repeatedIdle = 0
            self.order = ''
        else :
            parent_conn, child_conn = Pipe()
            #rfidReader = Process(target = read, args=(child_conn,))
            #rfidReader.daemon = True
            #rfidReader.start()
            self.uid = parent_conn.recv()
            if self.uid == "69688e3b":
                self.uid = "0123"
            if self.uid :
                buzzerProcess = Process(target = buzz)
                buzzerProcess.start()
                self.unlockMachine()
