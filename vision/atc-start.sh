#!/bin/bash
echo "path" $PYTHONPATH
echo "power on" | bluetoothctl
echo "project4" | sudo -S sh -c 'echo 79 > /sys/class/gpio/export; echo out > /sys/class/gpio/gpio79/direction; echo 1 > /sys/class/gpio/gpio79/value'
echo starting
/home/atc/archiconda3/bin/python3 /home/atc/Desktop/ATC/vision/main.py
echo done
echo "project4" | sudo -S sh -c 'echo 0 > /sys/class/gpio/gpio79/value'
