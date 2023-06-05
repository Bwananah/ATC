import threading
import time
import random
import subprocess


#voices = ["ATC/vision/Voices/voice0.wav",
#	"ATC/vision/Voices/voice1.mp3",
#	"ATC/vision/Voices/voice2.mp3",
#	"ATC/vision/Voices/voice3.mp3",
#	"ATC/vision/Voices/voice4.mp3",
#	"ATC/vision/Voices/voice5.mp3",
#	"ATC/vision/Voices/voice6.mp3",
#	"ATC/vision/Voices/voice7.mp3",
#	"ATC/vision/Voices/voice8.mp3",
#	"ATC/vision/Voices/voice9.mp3",
#	"ATC/vision/Voices/voice10.mp3",
#	"ATC/vision/Voices/voice11.mp3",
#	"ATC/vision/Voices/voice12.mp3"]

voices = [
    "Voices/voice0.wav",
	"Voices/voice1.mp3",
	"Voices/voice2.mp3",
	"Voices/voice3.mp3",
	"Voices/voice4.mp3",
	"Voices/voice5.mp3",
	"Voices/voice6.mp3",
	"Voices/voice7.mp3",
	"Voices/voice8.mp3",
	"Voices/voice9.mp3",
	"Voices/voice10.mp3",
	"Voices/voice11.mp3",
	"Voices/voice12.mp3"]

""" Reminds the Challenger periodically or when an obstacle is detected """
class Reminder():
    def __init__(self, interval, min_delay):
        self.interval = interval  # Random periodic reminder interval : [min, max] (in seconds)
        self.min_delay = min_delay  # Time that needs to elapse before another reminder can be played (in seconds)

        self.timer = None
        self.time_when_reminded = 0
        self.current_time = 0
        self.is_running = False

    # Plays reminder audio if enough time passed (either alert or reminder)
    def remind(self, isAlert):
        self.current_time = time.perf_counter()
	    
        # only notify if it's been long enough since last reminded
        if (self.current_time - self.time_when_reminded >= self.min_delay):
            rand_voice = random.choice(voices)
            if (isAlert):
                print("Alert")
                subprocess.call(["/usr/bin/vlc", "--intf","dummy","--play-and-exit", rand_voice], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print("Reminder")
                subprocess.call(["/usr/bin/vlc","--intf","dummy","--play-and-exit", voices[0]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # reset reminder
            self.stop()
            self.start()
            
            # reset times
            self.time_when_reminded = time.perf_counter()
            self.current_time = self.time_when_reminded

    # Callback function for the reminder
    def run(self):
        self.remind(False)

    # Starts a new reminder timer
    def start(self):
        if not self.is_running:
            time_to_remind = random.random() * (self.interval[1] - self.interval[0]) + self.interval[0]  # random time in interval
            self.timer = threading.Timer(time_to_remind, self.run)  # call self.run when timer ends
            self.timer.start()
            self.is_running = True
    
    # Stops the reminder timer
    def stop(self):
        self.timer.cancel()
        self.is_running = False
