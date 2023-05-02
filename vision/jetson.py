import os
import wave
import bluetooth

def play_audio(file_path, device_name):
    # Open the WAV file
    with wave.open(file_path, 'rb') as audio_file:
        # Get the audio parameters
        audio_params = audio_file.getparams()

        # Get a Bluetooth socket
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        # Find the Bluetooth device
        devices = bluetooth.discover_devices()
        print(devices)
        target_device = None
        for device in devices:
            if bluetooth.lookup_name(device) == device_name:
                target_device = device
                break

        # Connect to the device
        if target_device:
            port = 1
            sock.connect((target_device, port))
            print('Connected to {}'.format(device_name))

            # Send the audio data
            sock.sendall(audio_file.readframes(audio_params.nframes))
            print('Audio sent')

            # Close the connection
            sock.close()
            print('Connection closed')
        else:
            print('Could not find device "{}"'.format(device_name))

# Example usage
play_audio('voice.wav', '88:C9:E8:9E:02:78')
