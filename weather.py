from dotenv import load_dotenv
import os
import requests
import json

class Weather:

    def __init__(self) -> None:
        load_dotenv()
        self.API_WEATHER_KEY = os.getenv('API_WEATHER_KEY')
    
    def loadCities(self) -> None:
        with open('cities.json', 'r') as file:
            self.cities = json.load(file)

    def findCity(self, message: str) -> str:
        for city in self.cities:
            if message.find(city.lower()) != -1:
                return city
        return "null"

    def getWeather(self, message: str) -> str:
        self.loadCities()
        city = self.findCity(message)
        if city == "null":
            return "Désolé, je n'ai pas compris. De quelle ville parlez-vous ?"
        print(city)
        data = self.apiRequest(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&&appid={self.API_WEATHER_KEY}")
        return self.printResponse(data, city)

    def apiRequest(self, url : str) -> object:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        return data
    
    def printResponse(self, data, city: str) -> str:
        temp = data['main']['temp']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        return f'La météo actuelle à {city} est de **{temp}°C**. Les températures maximales aujourd\'hui seront de **{temp_max}°C** et les minimales de **{temp_min}°C**.'
