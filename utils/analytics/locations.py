import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

number_of_vehicles = 0

st.set_page_config(
    page_title="Bussie Dashboard",
    page_icon="🚎",
    layout="wide")

st.title("Bussie API Dashboard")

st.subheader('All public transport movements in NL 🇳🇱')
st.metric(label="Number of vehicles tracked", value=number_of_vehicles)


with st.empty():
    while True:
        df = pd.pandas.read_json('https://bussie.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/API/V1/get_vehicles', orient='index')
        df = pd.DataFrame(df,columns=['linenumber','latitude', 'longitude'])
        st.map(df, zoom=13)
        number_of_vehicles = df.shape[0] 
        time.sleep(5)