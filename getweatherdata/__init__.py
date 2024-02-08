import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import requests
import os
import matplotlib.pyplot as plt
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    city = req.params.get('city')
    if not city:
        try:
            req_body = req.get_json()
            city = req_body.get('city')
        except ValueError:
            pass

    if city:
        KEY = os.getenv("KEY")
        URL = "http://api.openweathermap.org/data/2.5/forecast"
        response = requests.get(f"{URL}?q={city}&appid={KEY}&units=metric")

        if response.status_code == 200:
            data = response.json()
            temperature = data['list'][0]['main']['temp']
            weather_condition = data['list'][0]['weather'][0]['description']
            return func.HttpResponse(json.dumps({"city": city, "temperature": temperature, "condition": weather_condition}), status_code=200)
        else:
            return func.HttpResponse("Failed to fetch weather data", status_code=response.status_code)
    else:
        return func.HttpResponse("Please enter a city", status_code=400)