import tensorflow as tf
import numpy as np
import discord
from weather import Weather
from groceries import Groceries
from dotenv import load_dotenv
import os

from discord.ext import commands
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

vocabulary = []
classes = []

training_data = [
    ("Comment ça va ?", "Très bien, merci. Et toi ?"), 
    ("Comment tu vas ?", "Je vais bien, merci. Et toi ?"),
    ("Salut", "Salut, tu vas bien ?"),
    ("Bonjour", "Salut, tu vas bien ?"),
    ("Hello", "Salut, tu vas bien ?"),
    ("Yo", "Salut, tu vas bien ?"),
    ("Salut !", "Salut, tu vas bien ?"),
    ("Comment t'appelles-tu ?", "Je m'appelle Friday."),
    ("Comment tu t'appelles ?", "Je m'appelle Friday."),
    ("Quel est ton nom ?", "Je m'appelle Friday."), 
    ("Que fais-tu ?", "Rien de spécial, et toi ?"),
    ("Tu fais quoi ?", "Rien de spécial, et toi ?"),
    ("Ajoute à ma liste de courses.", "liste-courses"),
    ("Ajoute du poulet à ma liste de courses.", "liste-courses"),
    ("Ajoute du objet à ma liste de courses.", "liste-courses"),
    ("Ajoute à ma liste de courses", "liste-courses"),
    ("Mets à ma liste de courses.", "liste-courses"),
    ("Rajoute à ma liste de courses.", "liste-courses"),
    ("Donne moi ma liste de courses.", "get-liste-courses"),
    ("Quelle est ma liste de courses.", "get-liste-courses"),
    ("Envoie ma liste de courses.", "get-liste-courses"),
    ("Peux-tu me dire ma liste de courses.", "get-liste-courses"),
    ("Rappelle moi ma liste de courses.", "get-liste-courses"),
    ("Qu'ai-je dans ma liste de courses ?", "get-liste-courses"),
    ("Qu'est ce qu'il y a dans ma liste de courses ?", "get-liste-courses"),
    ("Supprime objet de ma liste de courses", "remove-liste-courses"),
    ("Enlève objet de ma liste de courses", "remove-liste-courses"),
    ("Enlève l'objet de ma liste de courses", "remove-liste-courses"),
    ("Enlève le objet de ma liste de courses", "remove-liste-courses"),
    ("Retire de ma liste de courses", "remove-liste-courses"),
    ("Supprime de ma liste de courses", "remove-liste-courses"),
    ("Quelle est la météo ?", "meteo"),
    ("Quel temps fait-il ?", "meteo"),
    ("Météo à ?", "meteo"),
    ("Météo à ville", "meteo"),
    ("Météo aujourd'hui à", "meteo"),
    ("Météo", "meteo"),
    ("Quel temps fait-il aujourd'hui ?", "meteo"),
    ("Je suis triste", "Je suis désolé de l'apprendre, j'espère que ce n'est pas trop grave."),
    ("J'ai tué quelqu'un", "Tu viens de me dire que tu as tué quelqu'un ? Je vais alerter la police."),
    ("J'ai assassiné quelqu'un", "Tu viens de me dire que tu as tué quelqu'un ? Je vais alerter la police."),
    ("J'ai coupé la main à quelqu'un", "Tu viens de me dire que tu as tué quelqu'un ? Je vais alerter la police."),
    ("J'ai tué ma tante", "Tu viens de dire de dire que tu as tué quelqu'un ? Je vais alerter la police."),
    ("Tu fais quoi aujourd'hui ?", "Rien de spécial, et toi ?"),
    ("Quel est ton plat préféré ?", "Je n'ai pas de préférence, je suis une intelligence artificielle."), 
    ("Quel est le sens de la vie ?", "Le sens de la vie est une question philosophique complexe."), 
    ("Que penses-tu de l'intelligence artificielle ?", "Je pense que l'intelligence artificielle a un grand potentiel."), 
    ("Que penses-tu de l'ia ?", "Je pense que l'intelligence artificielle a un grand potentiel."), 
    ("Qui est ton créateur ?", "Mon créateur s'appelle Raphaël PERRIN."), 
    ("Qui t'a créé ?", "Mon créateur s'appelle Raphaël PERRIN."),
    ("Quel est ton film préféré ?", "Je ne peux pas regarder de films, je suis un programme informatique."), 
    ("Qui a gagné la dernière Coupe du Monde ?", "La France a remporté la dernière Coupe du Monde."), 
    ("Quel est le plus haut sommet du monde ?", "Le mont Everest est le plus haut sommet du monde."), 
    ("Comment fonctionne la photosynthèse ?", "La photosynthèse est le processus par lequel les plantes convertissent la lumière en énergie."), 
    ("Quelle est la capitale de la France ?", "La capitale de la France est Paris."), 
    ("Quelle est la couleur du ciel ?", "La couleur du ciel peut varier, mais généralement elle est bleue."), 
    ("De quelle couleur est le ciel ?", "La couleur du ciel peut varier, mais généralement elle est bleue."), 
    ("Quel est ton sport préféré ?", "Je n'ai pas de sport préféré, je suis un programme informatique."), 
    ("C'est quoi ton sport préféré ?", "Je n'ai pas de sport préféré, je suis un programme informatique."), 
    ("Combien de planètes y a-t-il dans notre système solaire ?", "Il y a huit planètes dans notre système solaire."), 
    ("Quelle est la durée d'une journée sur Mars ?", "Une journée sur Mars dure environ 24 heures et 37 minutes."), 
    ("Combien de temps dure une journée sur Mars ?", "Une journée sur Mars dure environ 24 heures et 37 minutes."), 
    ("Quelle est la signification de la vie ?", "La signification de la vie peut varier d'une personne à l'autre."), 
    ("Que penses-tu de l'amour ?", "L'amour est un sentiment complexe et profond."), 
    ("T'en penses quoi de l'amour ?", "L'amour est un sentiment complexe et profond."), 
    ("Qui es-tu ?", "Je suis Friday, une intelligence artificielle spécialement entrainée pour répondre à tes questions."), 
    ("Tu es qui ?", "Je suis Friday, une intelligence artificielle spécialement entrainée pour répondre à tes questions."), 
    ("monnaie", "Désolé, je ne peux pas te transmettre l'argent gagné pour le moment. Attends que je fasse mon annonce quotidienne."), 
    ("money", "Désolé, je ne peux pas te transmettre l'argent gagné pour le moment. Attends que je fasse mon annonce quotidienne."), 
    ("argent", "Désolé, je ne peux pas te transmettre l'argent gagné pour le moment. Attends que je fasse mon annonce quotidienne."), 
    ("salaire", "Désolé, je ne peux pas te transmettre l'argent gagné pour le moment. Attends que je fasse mon annonce quotidienne."), 
    ("fdp", "Je ne te permets pas de m'insulter."), 
    ("ta mère", "Je ne te permets pas de m'insulter."), 
    ("tu es moche", "Je ne te permets pas de m'insulter."), 
    ("T'es vexé ?", "Je suis un programme informatique, je ne peux pas être vexé."), 
    ("Tu connais personne ?", "Je ne connais pas spécialement cette personne."), 
    ("Comment m'endormir vite ?", "Je ne connais pas la réponse à cette question pour le moment, mais j'apprends vite !"), 
]
for question, _ in training_data:
    words = question.lower().split()
    for word in words:
        if word not in vocabulary:
            vocabulary.append(word)

for _, response in training_data:
    classes.append(response)

vocabulary = list(set(vocabulary))


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
    
    input_vector = [idx for idx in input_vector if idx != -1]
    training_data_input.append(input_vector)
    training_data_target.append(classes.index(response))

max_sequence_length = 10 
training_data_input = pad_sequences(training_data_input, maxlen=max_sequence_length, padding='post')

training_data_target = np.array(training_data_target)

model = Sequential()

model.add(Embedding(input_dim=len(vocabulary), output_dim=128))

model.add(LSTM(128, return_sequences=True))

model.add(LSTM(128))

model.add(Dense(128, activation='relu'))

model.add(Dense(len(classes), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#model.load_weights('model_weights.h5')

model.fit(training_data_input, training_data_target, epochs=200)
model.save_weights('model_weights.h5')

model.summary()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents= intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if not message.content.startswith('!'):
        return
    if message.author == bot.user:
        return

    content = message.content.lower()
    content = content.replace("-", " ")
    content = content.replace("'", " ")
    content = content.replace(",", " ")
    content = content.replace("?", "")
    content = content[1:]
    encoded_message = [vocabulary.index(token) if token in vocabulary else -1 for token in content.split()]
    encoded_message = [idx for idx in encoded_message if idx != -1]
    encoded_message = pad_sequences([encoded_message], maxlen=max_sequence_length, padding='post')
    prediction = model.predict(encoded_message)
    predicted_index = np.argmax(prediction)

    if 0 <= predicted_index < len(classes):
        predicted_class = classes[predicted_index]
    else:
        predicted_class = "Désolé, je n'ai pas compris."
        await message.channel.send(predicted_class)
        return

    if predicted_class == "meteo":
        weather = Weather()
        await message.channel.send(weather.get_weather(content))
    elif predicted_class == "liste-courses":
        groceries = Groceries()
        await message.channel.send(groceries.add_grocery(content, message.author.id))
    elif predicted_class == "get-liste-courses":
        groceries = Groceries()
        await message.channel.send(groceries.get_groceries(message.author.id))
    elif predicted_class == "remove-liste-courses":
        groceries = Groceries()
        print(message.content)
        await message.channel.send(groceries.remove_grocery(content, message.author.id))

    else :
        await message.channel.send(predicted_class)

bot.run(DISCORD_TOKEN)