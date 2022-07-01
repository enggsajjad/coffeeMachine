import logging

BOARD = 1
OUT = 0
IN = 1
PUD_DOWN = 0
PUD_UP = 1
HARD_PWM = 0
SERIAL = 0
UNKNOWN = 0
PUD_OFF = 0
BOTH = 0
RISING = 0
FALLING = 0
BCM = 0

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

inputOptions = {
    # 40: 0, # unlock
    35: {'value': 0, 'desc': 'W'}, # water switch 
    29: {'value': 0, 'desc': 'F1'}, # waterflow 1
    31: {'value': 0, 'desc': 'F2'}, # waterflow 2
    33: {'value': 0, 'desc': 'G'}, # grinder
}

values = []

def init():
    with open('/home/pi/CoffeeMachine/UI/logs/2019-07-15.txt') as f:
        content = f.readlines()

    global values
    for line in content:
        if not line[0] == '[':
            values.append(line.split(' ')[1][1:-2].split(','))
    next()

def next():
    global values
    global inputOptions

    new_inputs = values.pop(0)
    inputOptions[35]['value'] = int(new_inputs[0])
    inputOptions[29]['value'] = int(new_inputs[1])
    inputOptions[31]['value'] = int(new_inputs[2])
    inputOptions[33]['value'] = int(new_inputs[3])
    
    logger.info("Next gpio inputs [W,F1,F2,G]: [%s]", ",".join(map(str, new_inputs)))

def parseLog(line):
    return 

def setmode(mode):
    logger.debug("Setmode called: %i", mode)
def setup(a, b, pull_up_down=PUD_DOWN):
    logger.debug("Setup %i %s", a, b)
def output(a, b=1):
    logger.debug("Output %i %i", a, b)
def cleanup():
    logger.debug("Cleaning up")
def setwarnings(flag):
    logger.debug("Flags")
def input(pin):
    if pin in inputOptions:
        got = inputOptions[pin]
        logger.debug("Read %s = %i", got['desc'], got['value'])
        return got['value']
    else:
        logger.error("No input set for pin %i", pin)
        return 0

# init()

class I2C():
    pass

class SPI():
    pass