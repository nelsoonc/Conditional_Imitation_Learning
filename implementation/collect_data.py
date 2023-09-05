"""
Training data-collection script: End-to-end Driving using Conditional Imitation Learning
Run on: NVIDIA Jetson TX2 (1/10-scale RC Car)
Data acquisition at ~10 FPS
@author: nelsoonc

Undergraduate Thesis
Bandung Institute of Technology, Mechanical Engineering 2017
"""

"""
Receiver Trasped 16C
Channel 1: throttle
Channel 2: steering
Channel 6: save
Channel 7: mode
Channel 11: command
"""

import os
import shutil
import numpy as np
import pandas as pd
import cv2
import serial
import Adafruit_PCA9685
import pyrealsense2 as rs


# Initialize Arduino using port /dev/ttyACM0 or static name
arduino = serial.Serial('/dev/ArduinoNano', 9600, timeout=1)
arduino.flush()

# Initialize the PCA9685 using the default address (0x40).
# There are 2 I2C bus number in Jetson TX2, we're using number 1 here
pca9685 = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
THROTTLE_CHANNEL = 0
STEERING_CHANNEL = 1
GEAR_CHANNEL = 3
THROTTLE_PWM = 345
GEAR_PWM = 350  # Low gear
# Set frequency to 50hz, because frequency from receiver is 50 Hz.
pca9685.set_pwm_freq(50)

# Configure camera depth and color streams
wC, hC = (640, 360)
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, wC, hC, rs.format.bgr8, 30)
# Start streaming
pipeline.start(config)

# Variable initialization and PARAMETERS
image_filename_list = []
throttle_list = []
steering_list = []
command_list = []
count = 0
PARENT_DIR = os.sep.join(os.getcwd().split(os.sep)[:-1])
IMAGE_PATH = os.path.join(os.getcwd(), 'dataset/images')
CSV_PATH = os.path.join(os.getcwd(), 'dataset/dataset.csv')
text_params = {'fontFace': cv2.FONT_HERSHEY_SIMPLEX,
               'fontScale': 0.7,
               'color': (0,0,255),
               'thickness': 1,
               'lineType': cv2.LINE_AA}

def pulse_to_bit(pulse):
    """
    Trasped-16C controller sends 50 Hz signal to receiver
    Convert pulseIn reading from Arduino to 12-bit-scale pulse length
    Then the pulse length info will be sent to PCA9685
    PCA9685 is sending 12-bit pwm (4096 steps)
    """
    duty_cycle = pulse/20000
    return int(duty_cycle*4095)

def pulse_to_mode(pulse):
    if pulse < 1400: # bottom
        mode = 'manual'
    elif pulse > 1400 and pulse < 1600:
        mode = 'neutral'
    elif pulse > 1600:
        mode = 'autonomous'

    return mode

def pulse_to_cmd(pulse):
    if pulse < 1400: # bottom
        command = 'left'
    elif pulse > 1400 and pulse < 1600:
        command = 'straight'
    elif pulse > 1600:
        command = 'right'

    return command

# Remove last saved dataset folder
if os.path.exists(IMAGE_PATH):
    shutil.rmtree(IMAGE_PATH)
os.makedirs(IMAGE_PATH)

pca9685.set_pwm(GEAR_CHANNEL, 0, GEAR_PWM)

# read 5 first line from Arduino to prevent error
for i in range(5):
    if arduino.in_waiting > 0:
        line = arduino.readline().decode('utf-8').rstrip()
    else:
        continue

# ======================================================== #
while True:
    # Wait for a color frame
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    if not color_frame:
        continue

    # Data in frame (matrix) form can't be showed on cv2 window
    # Convert images to numpy arrays
    color_image = np.asanyarray(color_frame.get_data())

    # Take data from Arduino (delay 40 ms)
    if arduino.in_waiting > 0:
        line = arduino.readline().decode('utf-8').rstrip()
        throttle = pulse_to_bit(int(line.split(',')[0]))
        steering = pulse_to_bit(int(line.split(',')[1]))
        mode = pulse_to_mode(int(line.split(',')[2]))
        command = pulse_to_cmd(int(line.split(',')[3]))
    else:
        continue
    # comment print function to speed up looping
    # print('throttle: {}, steering: {}, mode: {}, command: {}'.format(throttle, steering, mode, command))

    if mode == 'manual' and 150 < steering < 450:
        pca9685.set_pwm(THROTTLE_CHANNEL, 0, THROTTLE_PWM)
        pca9685.set_pwm(STEERING_CHANNEL, 0, steering)

        # Save throttle, steering, and image data to list
        count += 1
        image_filename = '{:05d}.jpg'.format(count)
        image_filename_list.append(image_filename)
        throttle_list.append(throttle)
        steering_list.append(steering)
        command_list.append(command)
        cv2.imwrite(IMAGE_PATH + '/' + image_filename, color_image)
        if count % 10 == 0:
            print('saving frames..')

    # Show images
    cv2.imshow('Camera', color_image)
    if cv2.waitKey(1) & 0xFF == 27:
        break


# Stop streaming
pipeline.stop()
arduino.close()
cv2.destroyAllWindows()

# Save dataset to csv file
if os.path.exists(CSV_PATH):
    os.remove(CSV_PATH)
print("Saving dataset to csv")
columns = ['filename', 'throttle', 'steering', 'command']
dataset_dict = {'filename': image_filename_list,
                'throttle': throttle_list,
                'steering': steering_list,
                'command' : command_list}
dataset = pd.DataFrame(dataset_dict)
dataset.to_csv(CSV_PATH, index=False, columns=columns)
print("Done")