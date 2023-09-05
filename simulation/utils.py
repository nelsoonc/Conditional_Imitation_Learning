"""
Script: contains utility methods needed to process data
@author: nelsoonc

Undergraduate Thesis
Bandung Institute of Technology, Mechanical Engineering 2017
"""

import cv2
import math
import numpy as np
import pandas as pd
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.utils import Sequence
from tensorflow.keras.initializers import Constant
from sklearn.model_selection import train_test_split
from imgaug import augmenters as iaa

IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNEL = 100, 320, 3
N_BIN = 2500

def load_data(csv_path, dataset_path, test_size):
    # center, left, right data are string correspond to the directory of images
    columns = ['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed']
    data = pd.read_csv(csv_path, header=0, names=columns)

    x = []
    drop_indexes = []

    print('Importing data...')
    print('[INFO] Total images before drop:', np.shape(data)[0])
    for i in range(data.shape[0]):
        if data['steering'][i] == 0:
            drop_indexes.append(i)
    np.random.shuffle(drop_indexes)
    drop_indexes = drop_indexes[N_BIN:]
    data.drop(data.index[drop_indexes], inplace=True)

    center_path = data['center'].values # converted to array
    y = data['steering'].values  # converted to array


    for i in range(data.shape[0]):
        img = cv2.imread(dataset_path + '/' + center_path[i].split('\\')[-1])
        x.append(img) # converted to 'list' since x = []

    x = np.array(x)
    X_train, X_valid, y_train, y_valid = train_test_split(x, y, test_size=test_size, shuffle=True)

    assert(x.shape[0] == y.shape[0]), 'The number of images is not equal to the number of labels'
    print('[INFO] Total images imported:', np.shape(data)[0])
    print('[INFO] Total training dataset:', np.shape(X_train)[0])
    print('[INFO] Total validation dataset:', np.shape(X_valid)[0])

    return X_train, X_valid, y_train, y_valid


def augment_image(img, steering):

    aug1 = lambda aug: iaa.Sometimes(0.4, aug)
    aug2 = lambda aug: iaa.Sometimes(0.1, aug)
    seq = iaa.Sequential([
        aug2(iaa.GaussianBlur((0, 1.5))),  # blur images with a sigma between 0 and 1.5
        aug2(iaa.AdditiveGaussianNoise(loc=0, scale=(0, 20))),  # add gaussian noise to images, per_channel=0.5
        aug1(iaa.Add((-40, 40))),  # change brightness of images (by -X to Y of original value), per_channel=0.4
        # aug1(iaa.Multiply((0.5, 1.5), per_channel=0.2)),  # change brightness of images (X-Y% of original value)
        aug2(iaa.LinearContrast((0.5, 1.5))),  # improve or worsen the contrast, per_channel=0.4
    ], random_order=True)
    img = seq.augment_image(img)
    # Applying horizontal flip with 50% propobality
    if np.random.rand() < 0.5:
        img = iaa.Fliplr(1.0).augment_image(img)
        steering = -steering

    return img, steering


def preprocess(img):

    img = img[60:,:,:]
    img = cv2.resize(img, (IMAGE_WIDTH,IMAGE_HEIGHT))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img = img/255

    return img


def preprocess_test(data, dim):
    X_test = np.empty([len(data), dim[0], dim[1], dim[2]])

    for i in range(len(data)):
        img = preprocess(data[i])
        X_test[i] = img

    return X_test

class DataGenerator(Sequence):

    def __init__(self, data, label, batch_size, dim, subset, shuffle):
        self.data = data
        self.label = label
        self.batch_size = batch_size
        self.dim = dim  # (height, width, channel)
        self.subset = subset
        self.shuffle = shuffle
        self.count = 0
        self.on_epoch_end()

    def __len__(self):
        # Denotes the number of batches per epoch / steps per epoch
        return int(np.floor(len(self.data) / self.batch_size))

    def __getitem__(self, index):
        # Generate one batch of data
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        data_batch = [self.data[k] for k in indexes] # converted to list
        label_batch = [self.label[k] for k in indexes] # converted to list
        X, y = self.__data_generation(data_batch, label_batch)

        return X, y

    def on_epoch_end(self):
        # Triggered once at the beginning and every epoch
        self.indexes = np.arange(len(self.data))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, data_batch, label_batch):
        # Generates data containing (batch_size) samples
        X = np.empty([self.batch_size, self.dim[0], self.dim[1], self.dim[2]])
        y = np.empty(self.batch_size)

        # Generate data and label
        for i in range(len(data_batch)):
            if self.subset == 'train':
                img, steering = augment_image(data_batch[i], label_batch[i])
                img = preprocess(img)
            if self.subset == 'valid':
                img = preprocess(data_batch[i])
                steering = label_batch[i]
            X[i] = img
            y[i] = steering

        return X, y

    def __next__(self):
        if self.count == self.__len__():
            self.count = 0
        result = self.__getitem__(self.count)
        self.count += 1

        return result


# Simplified Codevilla et al. Model
class Network(object):
    def __init__(self):
        self.count_conv = 0
        self.count_dropout = 0
        self.count_bn = 0
        self.count_dense = 0
        self.count_activation = 0
        self.output_dimension = {}

    def fc(self, x, units):
        self.count_dense += 1
        return Dense(units, bias_initializer=Constant(0.1), name='dense_' + str(self.count_dense))(x)

    def conv_block(self, x, filters, kernel_size, stride, padding):
        self.count_conv += 1
        self.count_bn += 1
        # self.count_dropout += 1
        conv_res = Conv2D(filters, kernel_size, strides=(stride, stride), padding=padding,
                          activation='relu', kernel_initializer='glorot_uniform', use_bias=True,
                          bias_initializer=Constant(0.1), name='conv2d_' + str(self.count_conv))(x)
        conv_res = BatchNormalization(-1, momentum=0.99, epsilon=0.001,
                                      name='bn_' + str(self.count_bn))(conv_res)
        # conv_res = Dropout(0.2, name='dropout_' + str(self.count_dropout))(conv_res)

        output = (math.floor((x.shape[1] - kernel_size) / stride) + 1,
                  math.floor((x.shape[2] - kernel_size) / stride) + 1,
                  filters)
        self.output_dimension['Conv' + str(self.count_conv)] = output

        return conv_res

    def fc_block(self, x, units):
        self.count_dense += 1
        self.count_activation += 1
        self.count_dropout += 1
        fc_res = Dense(units, bias_initializer=Constant(0.1), activation='relu',
                       name='dense_' + str(self.count_dense))(x)
        fc_res = Dropout(0.2, name='dropout_' + str(self.count_dropout))(fc_res)

        return fc_res

    def flatten(self, x):
        return Flatten(name='flatten')(x)

    def print_output_dimension(self):
        print(self.output_dimension)
