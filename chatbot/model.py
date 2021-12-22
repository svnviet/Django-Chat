# things we need for NLP
import nltk
from underthesea import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from keras.utils.np_utils import to_categorical
# things we need for Tensorflow
import numpy as np
import tensorflow as tf
import keras
from tensorflow import keras
from tensorflow.keras import layers
import random
import pickle
import json
import re
from django.conf import settings
from .models import ChatbotIntent

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

stop_words = ['bạn', 'ban', 'anh', 'chị', 'chi', 'em', 'shop', 'bot', 'ad']


class ChatBot():
    def __init__(self, *args, **kwargs):
        self.user_id = None

    def convert_to_no_accents(self, text):
        output = text
        for regex, replace in patterns.items():
            output = re.sub(regex, replace, output)
            output = re.sub(regex.upper(), replace.upper(), output)
        return output

    def save_model(self, json_data):
        trains = {}
        intents = json_data
        for one_intent in intents['nlu']:
            sentences = one_intent['examples']
            for sentence in sentences.split('\n'):
                trains[one_intent['intent']] = sentence
        classes = {}
        X_train = []
        y_train = []
        for i, (key, value) in enumerate(trains.items()):
            X_train += [word_tokenize(v, format="text") for v in value.split(' ')] + [convert_to_no_accents(v) for v in value.split(' ')]
            y_train += [i] * len(value.split(' ')) * 2
            classes[i] = key

        pickle.dump(classes, open(settings.PKL + "classes.pkl", "wb"))

        y_train = to_categorical(y_train)
        vectorizer = TfidfVectorizer()

        # save this
        X_train = vectorizer.fit_transform(X_train).toarray()
        pickle.dump(vectorizer, open(settings.PKL + "tfidf_vectorizer.pkl", "wb"))

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(8, input_dim=X_train.shape[1]))
        model.add(tf.keras.layers.Dense(8))
        model.add(tf.keras.layers.Dense(len(y_train[0]), activation='softmax'))
        callbacks = [
            keras.callbacks.ModelCheckpoint(settings.PKL + 'model.h5', save_best_only=True),
        ]
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(X_train, y_train, epochs=500, batch_size=8, callbacks=callbacks)
        model.save(settings.PKL + 'model.h5')
        return model

    def load_model(self, sentence):
        from underthesea import word_tokenize
        from fuzzywuzzy import fuzz

        classes = pickle.load(open(settings.PKL + "classes.pkl", "rb"))
        model = tf.keras.models.load_model(settings.PKL + 'model.h5')
        vectorizer = pickle.load(open(settings.PKL + "tfidf_vectorizer.pkl", "rb"))

        sentence = word_tokenize(sentence, format="text")
        results = model.predict(vectorizer.transform([sentence]).toarray())[0]
        results = np.array(results)
        idx = np.argsort(-results)[0]
        res = self.response(classes[idx], results[idx])
        return res

    def response(self, tag, _):
        from .views import purpose_nlu_json_data
        intents = purpose_nlu_json_data(self.user_id)
        for i in intents['nlu']:
            if i['intent'] == tag:
                return i['response']
