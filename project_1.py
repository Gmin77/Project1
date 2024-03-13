import requests
import json
from page1 import *
from page2 import *
import streamlit as st
import pandas as pd
import os

if 'page' not in st.session_state:
    st.session_state['page'] = 'HOME'

with st.sidebar:
    if st.button("HOME", type='primary', use_container_width=True): st.session_state['page']='HOME'
    if st.button("주문", use_container_width=True): st.session_state['page']='order'
    if st.button("지난 주문 내역", use_container_width=True): st.session_state['page']='record'

if st.session_state['page']=='HOME':
    home()
elif st.session_state['page']=='order':
    weather()
elif st.session_state['page']=='record':
    pass


