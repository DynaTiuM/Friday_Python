import tensorflow as tf
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Définir le vocabulaire et les classes
vocabulary = [
    'bonjour', 'comment', 'allez', 'quelle', 'est', 'météo', 'la', 'vous', 'je', 'vais', 'bien', 'merci', 'et', 'toi', 'salut', 'appelles', 'que', 
    'tu', 'tu', 'il', 'temps', 'quel', 'que', 'demain', 'fera', 'fais', 't', 'rien', 'de', 'spécial', 'm', 'appelle', 'friday', 
]

classes = [
    'Je vais bien, merci. Et toi ?', 'Je vais bien, merci. Et toi ?', 'Salut, tu vas bien ?', 'Je m\'appelle Friday.',
    'Rien de spécial, et toi ?', "Je ne peux pas te fournir la météo pour le moment, désolé.", "Je ne peux pas déterminer la météo de demain actuellement."
]
training_data = [
    ("Bonjour comment allez-vous ?", "Je vais bien, merci. Et toi ?"),
    ("Salut comment tu vas ?", "Je vais bien, merci. Et toi ?"),
    ("Salut", "Salut, tu vas bien ?"),
    ("Comment appelles-tu ?", "Je m'appelle Friday."),
    ("Que fais-tu ?", "Rien de spécial, et toi ?"),
    ("Quelle est la météo ?", "Je ne peux pas te fournir la météo pour le moment, désolé."),
    ("Quel temps fait-il ?", "Je ne peux pas te fournir la météo pour le moment, désolé."),
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
    input_vector = [vocabulary.index(token) if token in vocabulary else -1 for token in message_tokens]
    
    # Ignorer les mots qui ne sont pas dans le vocabulaire
    input_vector = [idx for idx in input_vector if idx != -1]
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

model.load_weights('model_weights.h5')

#model.fit(training_data_input, training_data_target, epochs=500)
#model.save_weights('model_weights.h5')
message = "Salut"

message = preprocess_text(message)

message_tokens = message.strip().split()
encoded_message = [vocabulary.index(token) if token in vocabulary else -1 for token in message_tokens]

# Ignorer les mots qui ne sont pas dans le vocabulaire
encoded_message = [idx for idx in encoded_message if idx != -1]

encoded_message = pad_sequences([encoded_message], maxlen=max_sequence_length, padding='post')

prediction = model.predict(encoded_message)

predicted_index = np.argmax(prediction)

if 0 <= predicted_index < len(classes):
    predicted_class = classes[predicted_index]
else:
    predicted_class = "Je n'ai pas compris"

print(predicted_class)
