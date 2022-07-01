import logging
import inspect
from enum import Enum, IntEnum, auto

class DispensingStatus(IntEnum):
    ALLOW = auto()
    WARN = auto()
    DENY = auto()

class Msg(Enum):
    # commands 
    CMD_PAUSE = auto()
    CMD_RESUME = auto()
    CMD_LOCK = auto()
    CMD_UNLOCK = auto()

    # buzzer
    CMD_BUZZ = auto()
    CMD_ALARM = auto()

    # events 
    E_FLOW_1_STARTED = auto()
    E_FLOW_1_STOPPED = auto()
    E_FLOW_2_STARTED = auto()
    E_FLOW_2_STOPPED = auto()
    E_WATER_LEVEL_HIGH = auto()
    E_WATER_LEVEL_LOW = auto()
    E_GRINDER_LOW = auto()

    # rfid
    E_GOT_ID = auto()

def receive_cmd(conn, bind=None):
    """Receive pause and resume command from parent.
        If pause command was received, the function blocks and waits for resume message"""
    # poll for new messages from parent process
    if conn.poll():
        receive_cmd_block(conn, bind)

def receive_cmd_block(conn, bind=None):
    frames = inspect.getouterframes(inspect.currentframe())
    calling_module = list(filter(lambda frame_info: frame_info.code_context is not None, frames))[2].frame.f_globals["__name__"]
    logger = logging.getLogger(calling_module + ":util")

    msg = conn.recv()
    logger.debug("Received command: %s", msg)
    if msg == Msg.CMD_PAUSE:
        # pause reading until maintenance mode is switched off
        while True:
            msg = conn.recv()
            logger.debug("Received command: %s", msg)
            if msg == Msg.CMD_RESUME:
                break
        logger.debug("Resuming...")
    elif bind and msg in bind:
        bind[msg]()

# def terminate_after_error():
#     LOG.critical("An error occured the application cannot recover from. Terminating...")
#     psutil.Process(os.getppid()).terminate()

def price_to_str(price):
    return "{:.2f}€".format(price / 100)

def str_to_price(price_str):
    return int(float(price_str[:-1]) * 100)