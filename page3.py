import streamlit as st
import time
import pandas as pd

@st.cache_data
def load_data():
    data = pd.read_csv("record_data.csv")
    st.dataframe(data)
