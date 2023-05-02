import subprocess
import time

while True:
    subprocess.call(["vlc", "--play-and-exit","voice.wav"])
    time.sleep(10)  # wait for 60 seconds before playing the audio again
