import time
import datetime
import logging
from PyQt5.QtCore import QThread

LOG = logging.getLogger(__name__)

class SchedulerThread(QThread):
    every_hours = 3 #starting 0:00AM
    tasks = []
    cond = lambda self: True

    def set_condition(self, cond):
        """Set a condition as a function that evaluates to True or False for executing the tasks."""
        self.cond = cond

    def add_task(self, method):
        self.tasks.append(method)

    def secs_next_time(self):
        """Calculates the seconds until the next time, triggered by every_hours. Returns time in seconds"""
        next_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(
            hours=self.every_hours - datetime.datetime.now().hour % 3)
        return next_time.timestamp() - time.time()

    def run(self):
        while True:
            if not self.cond():
                LOG.info("Condition False. Retry in 5 minutes.")
                time.sleep(300)
                continue
            LOG.info("Running scheduled tasks")
            for fn in self.tasks:
                fn()

            time.sleep(self.secs_next_time())
