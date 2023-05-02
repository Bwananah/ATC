import Jetson.GPIO as GPIO
import time

input_pin = 33  # Physical pin 7 on the Jetson Nano's 40-pin header

def button_callback(channel):
    if GPIO.input(channel) == GPIO.HIGH:
        print("Button was released, GPIO state is HIGH")
    else:
        print("Button was pressed, GPIO state is LOW")

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(input_pin, GPIO.IN)

    GPIO.add_event_detect(input_pin, GPIO.BOTH, callback=button_callback, bouncetime=200)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Terminating the script...")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
