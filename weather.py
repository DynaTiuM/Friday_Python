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
            if message.find(city) != -1:
                print("City found : " + city)
                return city
        return "null"

    def getWeather(self, message: str) -> str:
        self.loadCities()
        city = self.findCity(message)
        data = self.apiRequest(f"https://api.openweathermap.org/data/2.5/weather?q={city}&&appid={self.API_WEATHER_KEY}")
        return self.printResponse(data, city)

    def apiRequest(self, url : str) -> object:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        print(data)

        return data
    
    def printResponse(data, city: str) -> str:
        return 'La météo actuelle à {city} est de {data.main.temp}°C'
