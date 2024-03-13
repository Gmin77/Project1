import streamlit as st
import json
import requests
import os
from dotenv import load_dotenv

def weather():
    load_dotenv()

    st.title('지역별 기온 및 날씨 정보')

    selected_city_options = ['Washington', 'Seoul', 'Paris', 'Berlin', 'Roma', 'Tokyo']
    selected_city_index = st.selectbox('지역을 선택하세요', selected_city_options)

    st.write(f'선택한 지역은 : {selected_city_index}')

    city = selected_city_index
    lang = 'kr'
    apikey = os.getenv("OPENWEATHERMAP_API_KEY")

    api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric'

    result = requests.get(api)
    data = json.loads(result.text)

    col1, col2 = st.columns(2) # 2,2 형태로 계속 출력

    with col1 :
        st.write(f'City : {city}')
    
    with col2 :
        try:
            temperature = data['main']['temp']
            st.write(f'City Temperature : {temperature} ℃')
        except KeyError:
            st.error('API 응답에서 기대한 데이터가 없습니다.')
        except Exception as e:
            st.error(f'예외가 발생했습니다: {e}')

    # with col3 :
    #     st.write(f'City Weather : {data['weather'][0]['main']}')


    # if city == data['name'] :
    #     print('값이 일치합니다.')
    # else :
    #     print('값이 틀립니다.')