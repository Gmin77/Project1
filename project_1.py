from page1 import *
from page2 import *
from page3 import *
import streamlit as st

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

with st.sidebar:
    if st.button("OpenWeather API", type='primary', use_container_width=True): st.session_state['page']='home'
    if st.button("지역별 기온 및 날씨 정보", type='secondary', use_container_width=True): st.session_state['page']='weather'
    if st.button("지난 기온 데이터", type='secondary', use_container_width=True): st.session_state['page']='db'

if st.session_state['page']=='home':
    st.title('프로젝트 1')
    st.subheader('OPEN API를 활용한 날씨 웹')
    home()
    if st.button("Project"):
        st.write_stream(home)
elif st.session_state['page']=='weather':
    weather()
elif st.session_state['page']=='db':
    load_data()



