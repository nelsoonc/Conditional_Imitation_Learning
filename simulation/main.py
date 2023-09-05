"""
Main script: Autonomous Driving on Udacity Simulator
Run on: Asus GL503VD (GTX 1050)
@author: nelsoonc

Undergraduate Thesis
Bandung Institute of Technology, Mechanical Engineering 2017
"""

"""
Throttle [0, 1]: speed [0, 30] mph
Steering [-1, 1]: angle [-25, 25] degrees
"""

import os
import numpy as np
import socketio
import eventlet
from flask import Flask
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
from train import rmse, get_lr_metric
from utils import preprocess
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# DIRECTORY PATH
MODEL_PATH = 'models/simulation_model.h5'

# VARIABLE
MAX_SPEED = 25


# FOR REAL TIME COMMUNICATION BETWEEN CLIENT AND SERVER
sio = socketio.Server()
# FLASK IS A MICRO WEB FRAMEWORK WRITTEN IN PYTHON
app = Flask(__name__)  # '__main__'

# Executing in graph mode
@tf.function
def predict(input_tensor, model):
    return model(input_tensor)


@sio.on('telemetry')
def telemetry(sid, data):
    speed = float(data['speed'])
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = preprocess(image)
    image = np.array([image])
    steering = float(predict(image, model))

    throttle = 1.0 - abs(steering) - speed / MAX_SPEED
    print('{}, {}, {}'.format(steering, throttle, speed))
    sendControl(steering, throttle)


@sio.on('connect')
def connect(sid, environ):
    print('Connected', sid)
    sendControl(0, 0)

@sio.on('disconnect')
def disconnect(sid):
    print('Disconnect', sid)


def sendControl(steering, throttle):
    sio.emit('steer', data={
        'steering_angle': steering.__str__(),
        'throttle': throttle.__str__()
    }, skip_sid=True)


if __name__ == '__main__':
    print('Setting up..')
    model = load_model(MODEL_PATH, custom_objects={'rmse': rmse, 'lr': get_lr_metric})
    if model:
        print('Model loaded')
    app = socketio.Middleware(sio, app)
    # LISTEN TO PORT 4567
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
