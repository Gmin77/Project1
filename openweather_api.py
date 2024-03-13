import requests
import json
import pandas as pd
import os

from dotenv import load_dotenv

def get_weather_data():

    load_dotenv()
    city = "Seoul"
    apikey = os.getenv("OPENWEATHERMAP_API_KEY")
    lang = 'kr'
    api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric'

    result = requests.get(api)
    data = json.loads(result.text)

    print(data)

    df = pd.DataFrame(data['list'])
    df['dt'] = pd.to_datetime(df['dt'], unit='s')
    df.set_index('dt', inplace=True)

    return df