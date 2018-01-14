from __future__ import division, absolute_import
import re
import numpy as np
from nwhacks2018.client.ernn.dataset_loader import DatasetLoader
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected, flatten
from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d
from tflearn.layers.merge_ops import merge
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
from nwhacks2018.client.ernn.constants import *
from os.path import isfile, join
import random
import sys

class EmotionRecognition:

  def __init__(self):
    self.dataset = DatasetLoader()

  def build_network(self):
    # Smaller 'AlexNet'
    # https://github.com/tflearn/tflearn/blob/master/examples/images/alexnet.py
    print('[+] Building CNN')
    self.network = input_data(shape = [None, SIZE_FACE, SIZE_FACE, 1])
    self.network = conv_2d(self.network, 64, 5, activation = 'relu')
    #self.network = local_response_normalization(self.network)
    self.network = max_pool_2d(self.network, 3, strides = 2)
    self.network = conv_2d(self.network, 64, 5, activation = 'relu')
    self.network = max_pool_2d(self.network, 3, strides = 2)
    self.network = conv_2d(self.network, 128, 4, activation = 'relu')
    self.network = dropout(self.network, 0.3)
    self.network = fully_connected(self.network, 3072, activation = 'relu')
    self.network = fully_connected(self.network, len(EMOTIONS), activation = 'softmax')
    self.network = regression(self.network,
      optimizer = 'momentum',
      loss = 'categorical_crossentropy')
    self.model = tflearn.DNN(
      self.network,
      checkpoint_path = SAVE_DIRECTORY + 'Gudi_model_100_epochs_20000_faces',
      max_checkpoints = 1,
      tensorboard_verbose = 2
    )
    self.load_model()
    print("Network Built!")

  def load_saved_dataset(self):
    self.dataset.load_from_save()
    print('[+] Dataset found and loaded')

  def start_training(self):
    self.load_saved_dataset()
    self.build_network()
    if self.dataset is None:
      self.load_saved_dataset()
    # Training
    print('[+] Training network')
    self.model.fit(
      self.dataset.images, self.dataset.labels,
      validation_set = (self.dataset.images_test, self.dataset._labels_test),
      n_epoch = 10,
      batch_size = 500,
      shuffle = True,
      show_metric = False,
      snapshot_step = 10000,
      snapshot_epoch = True,
      run_id = 'emotion_recognition'
    )

  def predict(self, image):
    if image is None:
      return None
    image = image.reshape([-1, SIZE_FACE, SIZE_FACE, 1])
    return self.model.predict(image)

  def save_model(self):
    self.model.save(join(SAVE_DIRECTORY, SAVE_MODEL_FILENAME))
    print('[+] Model trained and saved at ' + SAVE_MODEL_FILENAME)

  def load_model(self):
    if True:#sisfile(join(SAVE_DIRECTORY, SAVE_MODEL_FILENAME)):
      self.model.load(join(SAVE_DIRECTORY, SAVE_MODEL_FILENAME))
      print('[+] Model loaded from ' + SAVE_MODEL_FILENAME)
    else:
      print("bum file name")


def show_usage():
  # I din't want to have more dependecies
  print('[!] Usage: python emotion_recognition.py')
  print('\t emotion_recognition.py train \t Trains and saves model with saved dataset')
  print('\t emotion_recognition.py poc \t Launch the proof of concept')

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    show_usage()
    exit()

  network = EmotionRecognition()
  if sys.argv[1] == 'train':
    network.start_training()
    network.save_model()
  elif sys.argv[1] == 'poc':
    import poc

  else:
    show_usage()
