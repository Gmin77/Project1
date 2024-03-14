import requests
import json
import pandas as pd
import os
import streamlit as st

from dotenv import load_dotenv

def api():

    selected_city_options = ['Washington', 'Seoul', 'Paris', 'Berlin', 'Roma', 'Tokyo', 'Manila', 'Budapest', 'Genova',
                                'Beijing', 'Moscow', 'Boston', 'Barcelona', 'Shanghai', 'Sydney', 'Amsterdam', 'Prague']
    selected_city_index = st.selectbox('지역을 선택하세요', selected_city_options)

    st.write(f'선택한 지역은 : {selected_city_index}')
    city = selected_city_index
    lang = 'kr'
    apikey = os.getenv("OPENWEATHERMAP_API_KEY")

    api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&units=metric'