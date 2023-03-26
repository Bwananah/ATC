import serial

# Define serial port and baud rate
ser = serial.Serial('/dev/ttyACM0', 115200)

print("Starting...")
while True:
    # Read data from serial port and print it
    data = ser.readline().decode().rstrip()
    print(data)
