import logging
import logging.handlers
import multiprocessing
import util
from multiprocessing import Process, Pipe
import time
# import pyqttest

FORMAT = '%(asctime)s %(levelname)s:%(name)s:%(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)#, filename="inputGPIO.log", filemode="w")

# logger = logging.getLogger("testing.py")
# formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# # handler = logging.handlers.SysLogHandler("/dev/log")
# handler = logging.FileHandler("./testing.log")
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)

def f(conn):
    logging.info("Started child")
    # while True:
    #     logger.info("Waiting for data")
    #     logger.info((time.perf_counter() - conn.recv()))
    while True:
        util.receive_cmd(conn)
        logging.info("running")
        time.sleep(1)

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()

    time.sleep(3)
    parent_conn.send(util.Msg.CMD_PAUSE)
    time.sleep(3)
    parent_conn.send(util.Msg.CMD_RESUME)
    time.sleep(3)
    parent_conn.send(util.Msg.CMD_PAUSE)
