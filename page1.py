import streamlit as st
import time

_TEXT_ = """
    Access current weather data for any location on Earth! 
    We collect and process weather data from different sources such as global and local weather models, satellites, radars and a vast network of weather stations. 
    Data is available in JSON, XML, or HTML format.
    """

def home():
    for word in _TEXT_.split(" "):
        yield word + " "
        time.sleep(0.03)
