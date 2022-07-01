import threading
import time


def callback():
    print("Finish")


timer = ResetableTimer(5, callback)
timer.start()
time.sleep(0.001)
timer.reset()
time.sleep(0.001)
timer.cancel()
