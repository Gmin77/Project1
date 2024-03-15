import streamlit as st
import json
import requests
import os
from dotenv import load_dotenv
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import folium
from streamlit_folium import folium_static

lang = 'kr'
apikey = os.getenv("OPENWEATHERMAP_API_KEY")

def weather():
    load_dotenv()
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title('지역별 기온 및 날씨 정보')
    print(f"Folium version: {folium.__version__}")

    selected_city_options = ['Seoul', 'Paris', 'Berlin', 'Roma', 'Tokyo', 'Manila', 'Budapest', 'Genova',
                            'Beijing', 'Moscow', 'Boston', 'Barcelona', 'Shanghai', 'Sydney', 'Amsterdam', 'Prague']
    selected_city_index = st.selectbox('Select City', selected_city_options)

    st.write(f'Choose City : {selected_city_index}')

    city = selected_city_index
    api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&units=metric'
    # st.set_option('deprecation.showPyplotGlobalUse', False)

    result = requests.get(api)
    data = json.loads(result.text)

    if 'main' in data and 'weather' in data:
        location = data['name']
        temperature = data['main']['temp']
        weather_status = data['weather'][0]['main']

        # Folium을 사용하여 지도에 위치 표시하기
        m = folium.Map(location=[data['coord']['lat'], data['coord']['lon']], zoom_start=10)
        folium.Marker(location=[data['coord']['lat'], data['coord']['lon']], popup=f'{location}: {temperature}℃, {weather_status}').add_to(m)
        print(folium_static(m))
    else:
        st.write('City not found')

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
        st.write(f'Lowest Temperature : {data['main']['temp_min']} ℃')
       
    with col4 :
        st.write(f'Highest Temperature : {data['main']['temp_max']} ℃')

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
    date_check ={} # 값을 추가해줄 딕셔너리
    max_temp = {}
    min_temp = {}

    if "list" in datas :
        for forecast in datas['list'] :
            data_string = forecast['dt_txt']
            date_object = datetime.datetime.strptime(data_string, '%Y-%m-%d %H:%M:%S')
            day = date_object.strftime('%d')  # day만 출력 
            # print(f'Date: {date_object.date()}, Day: {day}')

            # if date_object == day :
            #     date_check[day] = forecast['dt_txt'].index
            
            if day not in date_check:
                date_check[day] = [datas['list'].index(forecast)]
            else:
                 date_check[day].append(datas['list'].index(forecast))  #해당 날짜를 구분하여 index의 길이를 측정하여 갯수파악

        for day, index in date_check.items(): # 딕셔너리 day, index의 값을 출력
            print(f"Date: {day}, Index: {index}")

        date_check1 = list(date_check.items())
        length = len(date_check1)

        for i in range(length):
            key, value = date_check1[i]
            # print(f"{key}, {value}")

        for key in date_check.keys():
            values = date_check[key]
            for idx, value in enumerate(values, start=1):
                print(f"{int(key)}day: {value}")
                check_list = datas['list'][value]
                check_list1 = check_list['main']['temp_min'] #최저온도
                check_list2 = check_list['main']['temp_max'] #최대온도
                # print(check_list)
                # print('최저 온도 :',check_list1,'°C')
                # print('최대 온도 :',check_list2,'°C')
                
                 # 최고온도와 최저온도를 딕셔너리에 저장
                if key not in max_temp:
                    max_temp[key] = check_list2
                elif check_list2 > max_temp[key]:
                    max_temp[key] = check_list2

                if key not in min_temp:
                    min_temp[key] = check_list1
                elif check_list1 < min_temp[key]:
                    min_temp[key] = check_list1

                print(max_temp)
                print(min_temp)

        print("최고 온도:")
        for key, value in max_temp.items():
            print(f"{key}: {value}°C")

        print("최저 온도:")
        for key, value in min_temp.items():
                print(f"{key}: {value}°C")
                

    df_max = pd.DataFrame(max_temp.items(), columns=['Date', 'Max Temp'])
    df_min = pd.DataFrame(min_temp.items(), columns=['Date', 'Min Temp'])

    print(df_max)
    print(df_min)

    plt.figure(figsize=(10, 6))
    plt.plot(df_max['Date'], df_max['Max Temp'], label='Max Temperature', marker='*')
    plt.plot(df_min['Date'], df_min['Min Temp'], label='Min Temperature', marker='*')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Weekly Temperature Forecast')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # plt.show() 대신에 st.pyplot() 사용
    st.pyplot()

    # fig, ax = plt.subplots()
    # df_max.plot(ax=ax)
    # df_min.plot(ax=ax)
    # ax.set_xlabel('날짜')
    # ax.set_ylabel('온도')
    # ax.set_title('최고 및 최저 온도 추이')

    # st.pyplot(fig)

    # df = pd.DataFrame({
    #     'Date': dates,
    #     'Max Temperature': temp_max_value,
    #     'Min Temperature': temp_min_value
    # })

    # # 날짜를 인덱스로 설정
    # df.set_index('Date', inplace=True)

    # # 바 차트 그리기
    # st.bar_chart(df)

