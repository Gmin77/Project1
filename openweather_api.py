import requests
import json
import pandas as pd
import os

def get_weather_data():
    city = "Seoul"
    api_key = os.getenv('apikey')
    lang = 'kr'
    api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang={lang}&units=metric'

    result = requests.get(api)
    data = json.loads(result.text)

    df = pd.DataFrame(data['list'])
    df['dt'] = pd.to_datetime(df['dt'], unit='s')
    df.set_index('dt', inplace=True)

    return df