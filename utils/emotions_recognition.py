import numpy as np
import cv2
from keras.models import load_model
import keras.backend as K

class EmotionRecognizer:
    
    def __init__(self, face_detector_path, model_path, session, graph):
        self.face_detector = cv2.CascadeClassifier(face_detector_path)
        self.sess = session
        self.graph = graph
        # Se carga la red neuronal ya entrenada
        with self.graph.as_default():
            K.set_session(session)
            self.model = load_model(model_path)

        self.emotions_dict = {0:'anger',1:'fear',2:'happiness',3:'sadness',4:'surprise',5:'neutral'}

    def recognize(self, img):
        results = {'main_emotion': '', 'probabilities': {}}
        # Se pasa la imagen a blanco y negro y a 48x48
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        # Se identifica la region del rostro
        faces = self.get_faces(img)
        if (len(faces) > 0):
            # Solo se va a utilizar un rostro
            x, y, w, h = faces[0]
            # Se recorta la imagen para utilizar solo la region del rostro
            face = img[y:y + h, x:x + w]
            face = cv2.resize(face, (48, 48))
            face = np.multiply(face, 1 / 255)
            with self.graph.as_default():
                K.set_session(self.sess)
                predictions = self.model.predict(np.reshape(face, [1, face.shape[0], face.shape[1], 1]))
            results['main_emotion'] = self.emotions_dict[np.argmax(predictions)]

            for i, p in enumerate(predictions[0]):
                results['probabilities'][self.emotions_dict[i]] = float(p)

        return results

    def get_faces(self, img):
        return self.face_detector.detectMultiScale(
            img,
            scaleFactor=1.1,
            minNeighbors=7,
            minSize=(100, 100)
        )