import requests
import json
import pandas as pd

def get_weather_data():
    city = "Seoul"
    apikey = '64d7ed0e91a9fbe556cf96ee9504c295'
    lang = 'kr'
    api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric'

    result = requests.get(api)
    data = json.loads(result.text)

    df = pd.DataFrame(data['list'])
    df['dt'] = pd.to_datetime(df['dt'], unit='s')
    df.set_index('dt', inplace=True)

    return df