import streamlit as st
import json
import requests
import os
from dotenv import load_dotenv
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

lang = 'kr'
apikey = os.getenv("OPENWEATHERMAP_API_KEY")


def weather():
    load_dotenv()

    selected_city_options = ['Washington', 'Seoul', 'Paris', 'Berlin', 'Roma', 'Tokyo', 'Manila', 'Budapest', 'Genova',
                            'Beijing', 'Moscow', 'Boston', 'Barcelona', 'Shanghai', 'Sydney', 'Amsterdam', 'Prague']
    selected_city_index = st.selectbox('지역을 선택하세요', selected_city_options)

    st.write(f'선택한 지역은 : {selected_city_index}')

    city = selected_city_index
    api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&units=metric'
    # st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title('지역별 기온 및 날씨 정보')

    result = requests.get(api)
    data = json.loads(result.text)

    col1, col2 = st.columns(2) # 2,2 형태로 계속 출력
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)

    with col1 :
        st.write(f'City : {city}')
    
    with col2 :
        try:
            st.write(f"Temperature : {data['main']['temp']} ℃")
        except KeyError:
            st.error('API 응답에서 기대한 데이터가 없습니다.')
        except Exception as e:
            st.error(f'예외가 발생했습니다: {e}')

    with col3 :
        st.write(f'temp_min : {data['main']['temp_min']} ℃')
       
    with col4 :
        st.write(f'temp_max : {data['main']['temp_max']} ℃')

    with col5 :
        st.write(f'Weather : {data['weather'][0]['main']}')

    with col6 :
        st.write(f'Description : {data['weather'][0]['description']}')

    with col7 :
        st.write(f'pressure : {data['main']['pressure']} ph')

    with col8 :
        st.write(f'humidity : {data['main']['humidity']} %')

    st.divider()
        
    st.header('5일 주기 기온차트')

    apis = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric'
    forecast_result = requests.get(apis)
    datas = json.loads(forecast_result.text)

    print(datas)

    dates = []
    temp_max_value = []
    temp_min_value = []

    if "list" in datas :
        for forecast in datas['list'] :
            data_string = forecast['dt_txt']
            date_object = datetime.datetime.strptime(data_string, '%Y-%m-%d %H:%M:%S')
            day_of_week = date_object.strftime('%d')  # 데이 출력
            print(f'Date: {date_object.date()}, Day: {day_of_week}')


        timestamp = forecast['dt']
        date = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        temp_max = forecast['main']['temp_max']
        temp_min = forecast['main']['temp_min']

        dates.append(date)
        temp_max_value.append(temp_max)
        temp_min_value.append(temp_min)

    plt.figure(figsize=(8, 5))
    plt.plot(dates, temp_max_value, label='Max Temperature', marker='*')
    plt.plot(dates, temp_min_value, label='Min Temperature', marker='*')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Weekly Temperature Forecast for {city}')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # plt.show() 대신에 st.pyplot() 사용
    st.pyplot()
    # df = pd.DataFrame({
    #     'Date': dates,
    #     'Max Temperature': temp_max_value,
    #     'Min Temperature': temp_min_value
    # })

    # # 날짜를 인덱스로 설정
    # df.set_index('Date', inplace=True)

    # # 바 차트 그리기
    # st.bar_chart(df)

