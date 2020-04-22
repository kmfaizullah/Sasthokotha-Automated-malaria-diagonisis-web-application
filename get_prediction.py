from __future__ import print_function
import math
from flask import Flask, request
from flask_cors import CORS

import cv2

import keras
from keras import backend as K
from keras.utils import np_utils
from keras.models import Sequential
from keras.models import model_from_json
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.contrib.keras.api.keras.models import Sequential
from tensorflow.keras.models import load_model

import pickle
import os
import json
import pandas as pd
import nltk
import numpy as np
import random
import string
import operator
from flask import render_template




def image_result():
    '''
       It accepts document and window size comming by post request.
       It returns co-occurence matrix as a json.
    '''
   
    #print(image)
    #image="C3thin_original_IMG_20150608_163029_cell_83_1_1.png"
    result=get_img_predict(str(image))
    print("result is " + resut)
    return result

def get_img_predict(image):
    '''
       It takes sentence of a documnent as input and calculates word frequency.
       It returns frequency as a sorted list.
    '''
    model=tf.keras.models.load_model('autoencoder_final_result_32.h5')
    height=32
    width=32

    img = cv2.imread(image)
    im = cv2.resize(img,(height,width))
    im =im/ 255.0
    image=np.asarray(im)
    image=image.reshape(1,32,32,3)
    predictions = model.predict(image)
    result=''
    if(np.argmax(predictions)==1):
        result="Parasitized"
    elif(np.argmax(predictions)==0):
        result="Uninfected"
    return result
