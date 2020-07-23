import os
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import base64
from utils.emotions_recognition import EmotionRecognizer
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
import numpy as np

sess = tf.Session()
graph = tf.get_default_graph()

app = Flask(__name__)
CORS(app)
face_detector_path = os.path.abspath(os.path.dirname(__file__)) + '/models/haarcascade_frontalface_default.xml'
emotion_network_path = os.path.abspath(os.path.dirname(__file__)) + '/models/emotions_net.h5'
emotions_recognizer = EmotionRecognizer(face_detector_path, emotion_network_path, sess, graph)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emotions/get_emotions', methods=['POST'])
def get_emotions():
    '''
        Recibe la imagen como un string de base 64
        Devuelve las emociones como un json
    '''
    base64_string = request.data
    image = Image.open(BytesIO(base64.b64decode(base64_string[22:])))
    emotions = emotions_recognizer.recognize(image)
    return json.dumps(emotions)

@app.route('/fruits/recognize', methods=['POST'])
def recognize_fruit():
    pass

if __name__ == '__main__':
    app.run(debug=True)