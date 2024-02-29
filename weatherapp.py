import click
import requests
import os
import matplotlib.pyplot as plt
from io import BytesIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json
import datetime


KEY= os.getenv("API_KEY") # Get the API key from the environment variable
STORAGE_CONNECTION_STRING = os.getenv("STORAGE_CONNECTION_STRING") # Get the storage connection string from the environment variable
CONTAINER_NAME = os.getenv("CONTAINER_NAME") # Get the container name from the environment variable


@click.command() # Defines a command
@click.option('--city', prompt='Your city') # Defines the main prompt
def get_weather(city):
    city = city.lower()
    # Provides URL to access the plot and current weather
    def print_weather_data(dc):
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{city}_weatherplot.png"
        click.echo("Creating weather plot...")
        click.echo(f"Weather plot created for {city} in {dc}")
        click.echo(f"Weather in {city}, {weather_data['sys']['country']}: {weather_data['weather'][0]['description']}")
        click.echo(f"Temperature: {weather_data['main']['temp']}°C")
        click.echo(f"Wind: {weather_data['wind']['speed']} m/s")
        click.echo(f"Next 14 day forecast: {blob_url}")
    # Collects the date and time the data was collected
    def collect_date():
        date_collected = response.json()['list'][0]['dt']
        date_collected = datetime.datetime.fromtimestamp(date_collected).strftime('%d-%m-%y %H:%M:%S')
        metadata = {"date_collected": date_collected}
        blob_client.set_blob_metadata(metadata=metadata)
        blob_properties = blob_client.get_blob_properties()
        metadata = blob_properties.metadata
        dc = metadata['date_collected']
        return dc
    # Request URL
    request_url = f"https://api.openweathermap.org/data/2.5/forecast/daily?q={city}&cnt=14&appid={KEY}&units=metric" # Forecast
    request_url2 = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric" # Current weather
    # Make the request
    response = requests.get(request_url)
    response2 = requests.get(request_url2)
    # Check if the request was successful and print the weather
    if response.status_code == 200 and response2.status_code == 200:
        # Parses weather data for plotting
        temps = [item['temp']['day'] for item in response.json()['list']] # Forecast
        weather_data = response2.json() # Current weather
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
            if click.confirm(f"{city}_weatherplot.png already exists. Do you want to update?"):
                blob_client.upload_blob(bytes_io, overwrite=True)
                dc= collect_date()
                print_weather_data(dc)
            else:
                print("Weather plot not updated.")
                blob_properties = blob_client.get_blob_properties()
                metadata = blob_properties.metadata
                dc = metadata['date_collected']
                print_weather_data(dc)
        else:
            blob_client.upload_blob(bytes_io)
            collect_date()
            dc = collect_date()
            print_weather_data(dc)
    
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