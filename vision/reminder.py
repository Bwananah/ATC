import threading
import time
import random
import subprocess

class Reminder():
    def __init__(self, interval, min_delay):
        self.interval = interval
        self.min_delay = min_delay

        self.timer = None
        self.time_when_reminded = 0
        self.current_time = 0
        self.is_running = False

    def remind(self, isAlert):
        self.current_time = time.perf_counter()

        # only notify if it's been long enough since last reminded
        if (self.current_time - self.time_when_reminded >= self.min_delay):
            if (isAlert):
 #               print("Alert")
                subprocess.call(["vlc","--intf","dummy" ,"--play-and-exit", "voice.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            else:
#                print("Reminder")
                subprocess.call(["vlc", "--intf","dummy","--play-and-exit", "voice.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            
            # reset reminder
            self.stop()
            self.start()
            
            # reset times
            self.time_when_reminded = time.perf_counter()
            self.current_time = self.time_when_reminded

    def run(self):
        self.remind(False)

    def start(self):
        if not self.is_running:
            time_to_remind = random.random() * (self.interval[1] - self.interval[0]) + self.interval[0]
            self.timer = threading.Timer(time_to_remind, self.run)
            self.timer.start()
            self.is_running = True
        
    def stop(self):
        self.timer.cancel()
        self.is_running = False
