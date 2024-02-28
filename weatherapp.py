import click
import requests
import os
import matplotlib.pyplot as plt
from io import BytesIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json


KEY= os.getenv("API_KEY") # Get the API key from the environment variable
STORAGE_CONNECTION_STRING = os.getenv("STORAGE_CONNECTION_STRING") # Get the storage connection string from the environment variable
CONTAINER_NAME = os.getenv("CONTAINER_NAME") # Get the container name from the environment variable


@click.command() # Defines a command
@click.option('--city', prompt='Your city') # Defines the main prompt
def get_weather(city):
    city = city.lower()
    # Request URL
    request_url = f"https://api.openweathermap.org/data/2.5/forecast/daily?q={city}&cnt=14&appid={KEY}&units=metric" # Forecast
    request_url2 = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric" # Current weather
    # Make the request
    response = requests.get(request_url)
    response2 = requests.get(request_url2)
    # Check if the request was successful and print the weather
    if response.status_code == 200 and response2.status_code == 200:
        # Parses weather data for plotting
        temps = [item['temp']['day'] for item in response.json()['list']]
        weather_data = response2.json()
        # Generate plot
        plt.figure(figsize=(10, 6))
        plt.plot(temps, marker='o')
        plt.title(f"14 Day Temperature Forecast for {city}, {weather_data['sys']['country']}")
        plt.ylabel('Temperature (°C)')
        plt.xlabel('Days from now')
        
        # Save plot to a BytesIO object and rewinds bytes to start
        bytes_io = BytesIO()
        plt.savefig(bytes_io, format='png')
        plt.close()
        bytes_io.seek(0)
        
        # Upload to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=f"{city}_weatherplot.png")
        if blob_client.exists():
            print_weather_data()
        else:
            blob_client.upload_blob(bytes_io)
            print_weather_data()
        
        # Provides URL to access the plot and current weather
        def print_weather_data():
            blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{city}_weatherplot.png"
            click.echo(f"Weather plot created for {city}. You can access it here: {blob_url}")
            click.echo(f"Weather in {city}, {weather_data['sys']['country']}: {weather_data['weather'][0]['description']}")
            click.echo(f"Temperature: {weather_data['main']['temp']}°C")
            click.echo(f"Wind: {weather_data['wind']['speed']} m/s")
            click.echo(f"Next 14 day forecast: {blob_url}")    
    
    # Error handling
    elif response.status_code != 200:
        print("Sorry, there was a problem retrieving forecast data")
        print(f"Status code: {response.status_code}")
        return
    
    elif response2.status_code != 200:
        print("Sorry, there was a problem retrieving current weather data")
        print(f"Status code: {response2.status_code}")
        return
    else:
        print("Unknown error")
  

# Run the command  
if __name__ == '__main__':    
    print("Enter the city name to get the forecast and current weather")
    get_weather()