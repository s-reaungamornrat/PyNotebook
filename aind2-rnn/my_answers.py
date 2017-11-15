import numpy as np

from collections import Counter
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs    
    step_size = 1
    X = []
    y = series[window_size:]
    for i in range(0, len(series)-window_size, step_size):
      X.append(np.array(series[i:i+window_size]))    
    
    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(units=5, input_shape=(window_size, 1)))
    model.add(Dense(units=1))
    return model


### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):

    def is_typical_characters(ch, punctuation):
      if (ord(ch) <= ord('z') and ord(ch) >= ord('a')) or ch in punctuation or ch == ' ':
        return True
      return False
      
    punctuation = ['!', ',', '.', ':', ';', '?']
    characters = list(text)
    cleaned_characters = [ch for ch in characters if is_typical_characters(ch, punctuation)]
  
    return ''.join(cleaned_characters)

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs

    inputs = []
    outputs = []
    #outputs = text[slice(window_size,None,step_size)]
    for i in range(0, len(text)-window_size, step_size):
      inputs.append(text[i:i+window_size])
      outputs.append(text[i+window_size])

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(units=200, input_shape=(window_size, num_chars)))
    model.add(Dense(units=num_chars, activation='softmax'))
    return model
