from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np



labels_path = tf.keras.utils.get_file(
    'ImageNetLabels.txt',
    'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = np.array(open(labels_path).read().splitlines())

import json
import numpy
import requests

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    
    img_url = request.args.get('img_url', default = '*', type = str)
    filename = img_url.split('/')[-1].split('.')[0]
    file_ext = '.'+img_url.split('.')[-1]
    
    file = tf.keras.utils.get_file(filename+file_ext, img_url)

    # https://static01.nyt.com/images/2017/08/09/sports/09xp-siberianraceSUB1/09xp-siberianraceSUB1-articleLarge.jpg
    # https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg
    img = tf.keras.preprocessing.image.load_img(file, target_size=[224, 224])

    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.mobilenet.preprocess_input(
        x[tf.newaxis,...])
    
    data = json.dumps({"signature_name": "serving_default",
                   "instances": x.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://34.67.215.216:8501/v1/models/mobilenet:predict',
                                  data=data, headers=headers)
    predictions = numpy.array(json.loads(json_response.text)["predictions"])

    decoded = imagenet_labels[np.argsort(predictions)[0,::-1][:5]+1]


    return str(decoded)