import nltk

from nltk.stem.lancaster import LancasterStemmer
import pyttsx3
#from search import search
import numpy as np
import tflearn
import random
import pickle
import json
import inspect, os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
def getJsonPath():
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    path = os.path.join(path, 'data.json').replace("\\", "/")
    return path


def getPath(file):
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    path = os.path.join(path, file).replace("\\", "/")
    return path


stemmer = LancasterStemmer()
data = pickle.load(open("trained_data", "rb"))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

with open(getJsonPath()) as json_data:
    intents = json.load(json_data)

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='train_logs')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:

                    print("found in bag: %s" % w)

    return (np.array(bag))


model.load('./model.tflearn')

context = {}

ERROR_THRESHOLD = 0.25


def classify(sentence):
    results = model.predict([bow(sentence, words)])[0]
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list


def response(sentence):
    if sentence!=None:
        results = classify(sentence)
        if results:
            while results:
                for i in intents['intents']:
                    if i['tag'] == results[0][0]:

                            if i['tag']=='google':
                                message = random.choice(i['responses'])
                                search(sentence)



                            elif i['tag']==None:
                                message="sorry i can't understand"
                            elif i['tag']=="ok" :
                                 message=random.choice(i['responses'])



                            else:
                                message=random.choice(i['responses'])
                            engine.say(message)
                            engine.runAndWait()
                            return message

                results.pop(0)
