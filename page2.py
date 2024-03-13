import streamlit as st
import json
import requests
import os

def weather():

    st.title('지역별 기온 및 날씨 정보')

    selected_city_options = ['Washington', 'Seoul', 'Paris', 'Berlin', 'Roma', 'Tokyo']
    selected_city_index = st.selectbox('지역을 선택하세요', selected_city_options)

    st.write(f'선택한 지역은 : {selected_city_index}')

    city = selected_city_index
    api_key = os.getenv('apikey')
    lang = 'kr'
    api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang={lang}&units=metric'

    result = requests.get(api)
    data = json.loads(result.text)

    col1, col2 = st.columns(2) # 2,2 형태로 계속 출력

    with col1 :
        st.write(f'City : {city}')
    
    with col2 :
        st.write(f'City Temperature : {data['main']['temp']} ℃')

    # with col3 :
    #     st.write(f'City Weather : {data['weather'][0]['main']}')


    # if city == data['name'] :
    #     print('값이 일치합니다.')
    # else :
    #     print('값이 틀립니다.')