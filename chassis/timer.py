import threading
import time


class Timer:
    def __init__(self, period, func):
        self.func = func
        self.period = period

    def timer_loop(self):
        t = time.time()
        while True:
            t += self.period
            self.func()
            time.sleep(max(0, t-time.time()))

    def start(self):
        timer_thread = threading.Thread(target=self.timer_loop)
        timer_thread.daemon = True
        timer_thread.start()

