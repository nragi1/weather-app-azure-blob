# Weather App 

This Weather CLI App created through the click library utilises the OpenWeatherMap API to fetch and visualise temperature forecasts for the next 14 days and also display some current information about the weather such as temperature and wind speed for any city worldwide. The visualisation is generated as a plot utilising Matplotlib which is then uploaded to Azure Blob Storage. The image uploaded to Azure Blob Storage is sent as a link through the CLI where the user is able to click, download and view the plot.

## Purpose
Practice integrating Azure Services such as Blob Storage and practice my current python programming skills utilising libraries such as Click and Matplotlib.

## Key Features
- Prompt based city query
- 14-day Temperature Forecast
- Current Weather Insight
- Azure Blob Integration

## Requirements
- Python 3.9
- Azure subscription and storage account (The free tier should work fine)
- openweathermap account for the API (The free tier should work fine)

## Installation
1. Clone the repo to your machine and install the Python packages
```bash
git clone <repository_url>

pip install -r requirements.txt
```
2. Setup API:
  - Obtain your key from openweathermap
  - Obtain your container name and connection string from Azure Blob Storage
  - Set the environment variables
```bash  
set API_KEY=youropenweatherkey
set STORAGE_CONNECTION_STRING=yourconnectionstring
set CONTAINER_NAME=yourcontainername
```
## Customisation
This application can be customised easily by referring to the openweathermap API documentation and making the changes in the code.
