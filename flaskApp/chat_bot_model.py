import tensorflow as tf
from tensorflow.keras import Model, layers
import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import random
import json

with open("flaskApp\weightsNdata\intents.json") as file:
    data = json.load(file)

words = []
labels = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
    if intent['tag'] not in labels:
        labels.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w != "?" and w != "!"]
words = sorted(list(set(words)))

labels = sorted(labels)

stop_words = ['you', 'is', 'your','a']
#remove stop words
words = [w for w in words if w not in stop_words]

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return np.array([bag])

# Create TF Model.
# building NN here
num_classes = 10
num_features = 62
# Training parameters.
learning_rate = 0.1
training_steps = 2000
batch_size = 10
display_step = 100
# Network parameters.
n_hidden_1 = 8 # 1st layer number of neurons.
n_hidden_2 = 16 # 2nd layer number of neurons.
n_hidden_3 = 32
n_hidden_4 = 64

class NeuralNet(Model):
    # Set layers.
    def __init__(self):
        super(NeuralNet, self).__init__()
        # First fully-connected hidden layer.
        self.fc1 = layers.Dense(n_hidden_1, activation=tf.nn.relu)
        # First fully-connected hidden layer.
        self.fc2 = layers.Dense(n_hidden_2, activation=tf.nn.relu)
        # Second fully-connecter hidden layer.
        self.fc3 = layers.Dense(n_hidden_3, activation=tf.nn.relu)
        self.fc4 = layers.Dense(n_hidden_4, activation=tf.nn.relu)
        self.out = layers.Dense(num_classes, activation=tf.nn.softmax)

    # Set forward pass.
    def call(self, x, is_training=False):
        x = self.fc1(x)
        x = self.out(x)
        if not is_training:
            # tf cross entropy expect logits without softmax, so only
            # apply softmax when not training.
            x = tf.nn.softmax(x)
        return x

# Build neural network model.
neural_net = NeuralNet()

# Load trained weight
neural_net.load_weights(filepath="flaskApp\weightsNdata\chat_bot_prototype.ckpt")

class ChatBot:
    
    def __init__(self, input):
        self.input = input


    def chat(self):
        index = np.argmax( neural_net(bag_of_words(self.input, words)))
        tag = labels[index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        
        print(random.choice(responses))
        return random.choice(responses)
        

    

    pass


