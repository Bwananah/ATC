import time
import os
import subprocess

# Set the MAC address of your Bluetooth headphone
bluetooth_mac_address = "20:74:CF:82:39:41"

# Define the audio file to be played
audio_file = "voice.wav"

# Set up the Bluetooth audio connection
subprocess.call("bluetoothctl <<< 'connect " + bluetooth_mac_address + "' && exit", shell=True)

# Play the audio file
subprocess.call("cvlc --aout=alsa --alsa-audio-device=bluez " + audio_file, shell=True)

# Wait for the audio to finish playing
time.sleep(5)

# Disconnect from the Bluetooth audio device
subprocess.call("bluetoothctl <<< 'disconnect " + bluetooth_mac_address + "' && exit", shell=True)
