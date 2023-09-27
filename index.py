import tensorflow as tf
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Définir le vocabulaire et les classes
vocabulary = ['bonjour', 'comment','appelles', 'quelle', 'tu', 'allez', 'vous', 'je', 'vais', 'bien', 'merci', 'et', 'vous']
classes = ['Je vais bien, merci. Et vous ?', "Je m'appelle Bard.", "La capitale de la France est Paris.", "Aujourd'hui est le 27 septembre 2023."]

training_data = [
    ("Bonjour comment allez-vous ?", "Je vais bien, merci. Et vous ?"),
    ("Comment appelles-tu ?", "Je m'appelle Friday."),
]

def preprocess_text(text):
    text = text.lower()
    text = text.replace("-", " ")
    text = text.replace("'", " ")
    text = text.replace(",", " ")
    text = text.replace("?", "") 
    return text

training_data_input = []
training_data_target = []

for message, response in training_data:
    message = preprocess_text(message)
    message_tokens = message.strip().split()
    input_vector = [vocabulary.index(token) for token in message_tokens]
    training_data_input.append(input_vector)
    training_data_target.append(classes.index(response))

max_sequence_length = 10 
training_data_input = pad_sequences(training_data_input, maxlen=max_sequence_length, padding='post')

training_data_target = np.array(training_data_target)

model = Sequential()
model.add(Embedding(input_dim=len(vocabulary), output_dim=64))
model.add(LSTM(128, return_sequences=True)) 
model.add(LSTM(128))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(classes), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(training_data_input, training_data_target, epochs=20)

message = "Bonjour comment allez-vous ?"

message = preprocess_text(message)

message_tokens = message.strip().split()
encoded_message = [vocabulary.index(token) for token in message_tokens]

encoded_message = pad_sequences([encoded_message], maxlen=max_sequence_length, padding='post')

prediction = model.predict(encoded_message)

predicted_index = np.argmax(prediction)

if 0 <= predicted_index < len(classes):
    predicted_class = classes[predicted_index]
else:
    predicted_class = "Je n'ai pas compris"

print(predicted_class)
