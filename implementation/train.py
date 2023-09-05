"""
Model training script: End-to-end Driving using Conditional Imitation Learning
Run on: Asus GL503VD (GTX 1050, 24 GB RAM)
@author: nelsoonc

Undergraduate Thesis
Bandung Institute of Technology, Mechanical Engineering 2017
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
import tensorflow.keras.backend as K
from utils import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# DIRECTORY PATH
PARENT_DIR = os.sep.join(os.getcwd().split(os.sep)[:-1])
DATASET_PATH = os.path.join(os.getcwd(), 'dataset', 'images')
CSV_PATH = os.path.join(os.getcwd(), 'dataset', 'dataset.csv')

# PARAMETERS
IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNEL = 100, 220, 3
IMAGE_DIMENSION = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNEL)
BATCH_SIZE = 64
EPOCHS = 40
TEST_RATIO = 0.2
SHUFFLE = True
LEARNING_RATE = 0.001
DECAY_RATE = 0.001
params = {'batch_size': BATCH_SIZE,
          'dim': IMAGE_DIMENSION,
          'shuffle': SHUFFLE}
beta_1 = 0.7
beta_2 = 0.85

# VARIABLE
ml_train = []
ml_val = []
ml_lr = []
ms_train = []
ms_val = []
ms_lr = []
mr_train = []
mr_val = []
mr_lr = []


def build_model(image_dimension):

    inputs = Input(shape=image_dimension, name="input")

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
    outputs = network.fc_block(x, 128)

    return inputs, outputs

# Build the base architecture
inputs, outputs = build_model(IMAGE_DIMENSION)

def build_branches(command_flag):

    if command_flag == 'left':
        output_left = network.fc_block(outputs, 256)
        output_left = network.fc_block(output_left, 256)
        output_left = network.fc(output_left, 1)

        model_left = Model(inputs=inputs, outputs=output_left, name='model_left')
        return model_left
    elif command_flag == 'straight':
        output_straight = network.fc_block(outputs, 256)
        output_straight = network.fc_block(output_straight, 256)
        output_straight = network.fc(output_straight, 1)

        model_straight = Model(inputs=inputs, outputs=output_straight, name='model_straight')
        return model_straight
    elif command_flag == 'right':
        output_right = network.fc_block(outputs, 256)
        output_right = network.fc_block(output_right, 256)
        output_right = network.fc(output_right, 1)

        model_right = Model(inputs=inputs, outputs=output_right, name='model_right')
        return model_right
    else:
        print('Please specify the right command flag at branching')
        quit()

def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))

def get_lr_metric(optimizer):
    def lr(y_true, y_pred):
        return optimizer._decayed_lr(tf.float32)
    return lr



# Main training script
if __name__ == '__main__':

    # Read data from csv and split into train and validation dataset
    X_train1, X_valid1, y_train1, y_valid1 = load_data(CSV_PATH, DATASET_PATH,
                                                       command_flag='left',
                                                       test_size=TEST_RATIO)
    X_train2, X_valid2, y_train2, y_valid2 = load_data(CSV_PATH, DATASET_PATH,
                                                       command_flag='straight',
                                                       test_size=TEST_RATIO)
    X_train3, X_valid3, y_train3, y_valid3 = load_data(CSV_PATH, DATASET_PATH,
                                                       command_flag='right',
                                                       test_size=TEST_RATIO)

    'Build model'
    model_left = build_branches(command_flag='left')
    model_straight = build_branches(command_flag='straight')
    model_right = build_branches(command_flag='right')

    'Train model'
    adam1 = Adam(learning_rate=LEARNING_RATE, beta_1=beta_1, beta_2=beta_2, decay=DECAY_RATE)
    adam2 = Adam(learning_rate=LEARNING_RATE, beta_1=beta_1, beta_2=beta_2, decay=DECAY_RATE)
    adam3 = Adam(learning_rate=LEARNING_RATE, beta_1=beta_1, beta_2=beta_2, decay=DECAY_RATE)

    model_left.compile(optimizer=adam1, loss=rmse, metrics=[get_lr_metric(adam1)])
    model_straight.compile(optimizer=adam2, loss=rmse, metrics=[get_lr_metric(adam2)])
    model_right.compile(optimizer=adam3, loss=rmse, metrics=[get_lr_metric(adam3)])
    for epoch in range(EPOCHS):
        print('epoch:', epoch+1)
        print('left')
        h1 = model_left.fit(DataGenerator(X_train1, y_train1, subset='train', **params), epochs=1,
                            validation_data=DataGenerator(X_valid1, y_valid1, subset='valid', **params))
        print('straight')
        h2 = model_straight.fit(DataGenerator(X_train2, y_train2, subset='train', **params), epochs=1,
                                steps_per_epoch=70,
                                validation_data=DataGenerator(X_valid2, y_valid2, subset='valid', **params))
        print('right')
        h3 = model_right.fit(DataGenerator(X_train3, y_train3, subset='train', **params), epochs=1,
                             validation_data=DataGenerator(X_valid3, y_valid3, subset='valid', **params))

        ml_train.extend(h1.history['loss'])
        ml_val.extend(h1.history['val_loss'])
        ml_lr.extend(h1.history['lr'])
        ms_train.extend(h2.history['loss'])
        ms_val.extend(h2.history['val_loss'])
        ms_lr.extend(h2.history['lr'])
        mr_train.extend(h3.history['loss'])
        mr_val.extend(h3.history['val_loss'])
        mr_lr.extend(h3.history['lr'])

    'SAVE THE MODEL AS HDF5 FILE'
    model_left_name = 'model_left.h5'
    model_straight_name = 'model_straight.h5'
    model_right_name = 'model_right.h5'
    if not os.path.exists(os.path.join(os.getcwd(), 'models')):
        os.makedirs(os.path.join(os.getcwd(), 'models'))
    model_left.save(str(os.getcwd()) + '/models/' + model_left_name)
    model_straight.save(str(os.getcwd()) + '/models/' + model_straight_name)
    model_right.save(str(os.getcwd()) + '/models/' + model_right_name)

    # Save training history to csv
    print("")
    print("Saving training history")
    csv_left_filename = 'train_history_left.csv'
    csv_straight_filename = 'train_history_straight.csv'
    csv_right_filename = 'train_history_right.csv'
    history_dict1 = {'loss': ml_train,
                     'val_loss': ml_val,
                     'lr': ml_lr}
    history_dict2 = {'loss': ms_train,
                     'val_loss': ms_val,
                     'lr': ms_lr}
    history_dict3 = {'loss': mr_train,
                     'val_loss': mr_val,
                     'lr': mr_lr}
    history1 = pd.DataFrame(history_dict1)
    history2 = pd.DataFrame(history_dict2)
    history3 = pd.DataFrame(history_dict3)
    history1.to_csv('models/train_history_left.csv', index=False)
    history2.to_csv('models/train_history_straight.csv', index=False)
    history3.to_csv('models/train_history_right.csv', index=False)
    print("Done")

    # plt.plot(history_left.history['loss'])
    # plt.plot(history_left.history['val_loss'])
    # plt.legend(['Training', 'Validation'])
    # plt.title('Model Loss')
    # plt.xlabel('Epoch')
    # plt.ylabel('Loss')
    # plt.grid(True)
    # plt.savefig('models_home_history.png')
    # plt.show()
