import warnings # For annoying version warning
warnings.filterwarnings("ignore", message="Tuple timeout setting is deprecated")

import click
import requests
import os
import matplotlib.pyplot as plt
from io import BytesIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

KEY= os.getenv("API_KEY") # Get the API key from the environment variable
URL= "https://api.openweathermap.org/data/2.5/forecast?"
STORAGE_CONNECTION_STRING = os.getenv("STORAGE_CONNECTION_STRING") # Get the storage connection string from the environment variable
CONTAINER_NAME = os.getenv("CONTAINER_NAME") # Get the container name from the environment variable


@click.command() # Defines a command
@click.option('--city', prompt='Your city') # Defines the main prompt
def get_weather(city):
    # Request URL
    request_url = f"{URL}q={city}&appid={KEY}&units=metric"
    # Make the request
    response = requests.get(request_url)
    
    # Check if the request was successful and print the weather
    if response.status_code == 200:
        # Parses weather data for plotting
        temps = [item['main']['temp'] for item in response.json()['list']]
        
        # Generate plot
        plt.figure(figsize=(10, 6))
        plt.plot(temps, marker='o')
        plt.title(f"Temperature Forecast for {city}")
        plt.ylabel('Temperature (°C)')
        plt.xlabel('Time (3-hour intervals)')
        
        # Save plot to a BytesIO object and rewinds bytes to start
        bytes_io = BytesIO()
        plt.savefig(bytes_io, format='png')
        plt.close()
        bytes_io.seek(0)
        
        # Upload to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=f"{city}_weatherplot.png")
        blob_client.upload_blob(bytes_io, overwrite=True) # Overwrites duplicates
        
        # Provides URL to access the plot
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{city}_weatherplot.png"
        click.echo(f"Weather plot created for {city}. You can access it here: {blob_url}")
    
    # Error handling
    elif response.status_code != 200:
        print("Sorry, there was a problem retrieving the weather")
        print(f"Status code: {response.status_code}")
        return
  
  
# Run the command  
if __name__ == '__main__':
    print(f"API_KEY: {KEY}")
    print(f"Storage Connection String: {STORAGE_CONNECTION_STRING}")
    print(f"Container Name: {CONTAINER_NAME}")

    print("Enter the city name to get the weather")
    get_weather()