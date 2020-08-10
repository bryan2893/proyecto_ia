import numpy as np 
import cv2
from keras.models import load_model
import keras.backend as K

class FruitRecognizer:
    
    def __init__(self, model_path, session, graph):
        self.sess = session
        self.graph = graph
        with self.graph.as_default():
            K.set_session(session)
            self.model = load_model(model_path)

        self.fruits_dict = {
            0: {
                'name': 'Apple',
                'weight': 100,
                'calories': 52,
                'sugar': 10,
                'carbohydrates': 14
            },
            1: {
                'name': 'Banana',
                'weight': 118,
                'calories': 89,
                'sugar': 12,
                'carbohydrates': 23
            },
            2: {
                'name': 'Carambola',
                'weight': 124,
                'calories': 31,
                'sugar': 4,
                'carbohydrates': 7
            },
            3: {
                'name': 'Guava',
                'weight': 174,
                'calories': 68,
                'sugar': 9,
                'carbohydrates': 14
            },
            4: {
                'name': 'Kiwi',
                'weight': 76,
                'calories': 61,
                'sugar': 9,
                'carbohydrates': 15
            },
            5: {
                'name': 'Mango',
                'weight': 200,
                'calories': 60,
                'sugar': 14,
                'carbohydrates': 15
            },
            6: {
                'name': 'Orange',
                'weight': 154,
                'calories': 47,
                'sugar': 9,
                'carbohydrates': 12
            },
            7: {
                'name': 'Peach',
                'weight': 147,
                'calories': 39,
                'sugar': 8,
                'carbohydrates': 10
            },
            8: {
                'name': 'Pear',
                'weight': 178,
                'calories': 101,
                'sugar': 6,
                'carbohydrates': 27
            },
            9: {
                'name': 'Persimmon',
                'weight': 168,
                'calories': 127,
                'sugar': 21,
                'carbohydrates': 34
            },
            10: {
                'name': 'Pitaya',
                'weight': 150,
                'calories': 60,
                'sugar': 13,
                'carbohydrates': 22
            },
            11: {
                'name': 'Plum',
                'weight': 225,
                'calories': 30,
                'sugar': 7,
                'carbohydrates': 8
            },
            12: {
                'name': 'Pomegranate',
                'weight': 250,
                'calories': 83,
                'sugar': 14,
                'carbohydrates': 19
            },
            13: {
                'name': 'Tomato',
                'weight': 62,
                'calories': 18,
                'sugar': 3,
                'carbohydrates': 4
            },
            14: {
                'name': 'Muskmelon',
                'weight': 250,
                'calories': 34,
                'sugar': 8,
                'carbohydrates': 8
            }
        }


    def recognize(self, img):
        img = np.array(img)
        img = cv2.resize(img, (150, 150))
        img = np.multiply(img, 1 / 255)
        
        with self.graph.as_default():
            K.set_session(self.sess)
            predictions = self.model.predict(np.expand_dims(img, axis=0))
        
        predicted_fruit = np.argmax(predictions)
        confidence = np.max(predictions)
        nutritional_value = self.fruits_dict[predicted_fruit]

        return { 
            'confidence': str(np.round(confidence, 3)), 
            'results': nutritional_value 
        }
        