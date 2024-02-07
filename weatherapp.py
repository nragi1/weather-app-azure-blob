import click
import requests
import os

KEY= os.getenv("API_KEY") ## Get the API key from the environment variable
URL= "https://api.openweathermap.org/data/2.5/forecast?"

@click.command() ## Defines a command
@click.option('--city', prompt='Your city') ## Defines the main prompt
def get_weather(city):
    # Request URL
    request_url = f"{URL}q={city}&appid={KEY}&units=metric"
    # Make the request
    response = requests.get(request_url)
    
    # Check if the request was successful and print the weather
    if response.status_code == 200:
        data = response.json()
        print(f"Weather in {city}: {data['list'][0]['weather'][0]['description']}")
        print(f"Temperature: {data['list'][0]['main']['temp']}°C")
    elif response.status_code != 200:
        print("Sorry, there was a problem retrieving the weather")
        print(f"Status code: {response.status_code}")
        return
    
if __name__ == '__main__':
    print("Enter the city name to get the weather")
    get_weather()