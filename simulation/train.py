"""
Training script: Imitation learning on Udacity Simulator
Run on: Asus GL503VD (GTX 1050)
@author: nelsoonc

Undergraduate Thesis
Bandung Institute of Technology, Mechanical Engineering 2017
"""

import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
import tensorflow.keras.backend as K
from utils import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# DIRECTORY PATH
PARENT_DIR = os.getcwd()
DATASET_PATH = os.path.join(PARENT_DIR, 'dataset', 'IMG')
CSV_PATH = os.path.join(PARENT_DIR, 'dataset', 'driving_log.csv')

# PARAMETERS
BATCH_SIZE = 64
EPOCHS = 20
TEST_RATIO = 0.2
IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNEL = 100, 320, 3
IMAGE_DIMENSION = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNEL)
LEARNING_RATE = 0.001
DECAY_RATE = 0.0001
params = {'batch_size': BATCH_SIZE,
          'dim': IMAGE_DIMENSION,
          'shuffle': True}

# VARIABLE
loss = []
val_loss = []
lr = []


def build_model(image_dimension):

    inputs = Input(shape=image_dimension)

    global network
    network = Network()

    "conv1"
    xc = network.conv_block(inputs, 24, 5, 2, padding='VALID')
    "conv2"
    xc = network.conv_block(xc, 24, 3, 1, padding='VALID')
    "conv3"
    xc = network.conv_block(xc, 32, 3, 2, padding='VALID')
    "conv4"
    xc = network.conv_block(xc, 32, 3, 1, padding='VALID')
    "conv5"
    xc = network.conv_block(xc, 48, 3, 2, padding='VALID')
    "conv6"
    xc = network.conv_block(xc, 48, 3, 1, padding='VALID')
    "conv7"
    xc = network.conv_block(xc, 64, 3, 2, padding='VALID')
    "conv8"
    xc = network.conv_block(xc, 64, 3, 1, padding='VALID')

    x = network.flatten(xc)
    x = network.fc_block(x, 128)
    x = network.fc_block(x, 128)
    x = network.fc_block(x, 256)
    x = network.fc_block(x, 256)
    outputs = network.fc(x, 1)

    model = Model(inputs=inputs, outputs=outputs, name='simulation_model')

    return model


def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))

def get_lr_metric(optimizer):
    def lr(y_true, y_pred):
        return optimizer._decayed_lr(tf.float32)
    return lr


# Main script
if __name__ == '__main__':
    # Load data from csv and split into train and validation dataset
    X_train, X_valid, y_train, y_valid = load_data(CSV_PATH, DATASET_PATH,
                                                   test_size=TEST_RATIO)


    'Train model'
    model = build_model(image_dimension=IMAGE_DIMENSION)
    adam = Adam(learning_rate=LEARNING_RATE, beta_1=0.7, beta_2=0.85, decay=DECAY_RATE)
    model.compile(optimizer=adam, loss=rmse, metrics=[get_lr_metric(adam)])
    history = model.fit(DataGenerator(X_train, y_train, subset='train', **params), epochs=EPOCHS,
                        validation_data=DataGenerator(X_valid, y_valid, subset='valid', **params))

    # Save training history to list
    loss.extend(history.history['loss'])
    val_loss.extend(history.history['val_loss'])
    lr.extend(history.history['lr'])

    # Save training history to csv
    print("")
    print("Saving training history")
    csv_filename = 'train_history_left.csv'
    dataset_dict = {'loss': loss,
                    'val_loss': val_loss,
                    'lr': lr}
    dataset = pd.DataFrame(dataset_dict)
    dataset.to_csv('models/train_history.csv', index=False)
    print("Done")


    'SAVE THE MODEL AS HDF5 FILE'
    model_name = 'simulation_model.h5'
    model.save('models/' + model_name)
    if os.path.exists(os.getcwd() + '/models/' + model_name):
        print('#### MODEL SAVED AS \'{}\' ####'.format(model_name))
