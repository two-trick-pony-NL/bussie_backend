import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import pydeck as pdk

number_of_vehicles = 0

st.set_page_config(
    page_title="Bussie Dashboard",
    page_icon="🚎",
    layout="wide")

st.title("Bussie API Dashboard")

st.subheader('Public transport movements in NL 🇳🇱')

with st.empty():
    while True:
        df = pd.pandas.read_json('https://bussie.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/API/V1/get_vehicles', orient='index')
        df = pd.DataFrame(df,columns=['linenumber','latitude', 'longitude'])
        st.pydeck_chart(pdk.Deck(
            tooltip ={
                "html":
                    "<b>Line:</b>{linenumber}<br/>",
                "style": {
                    "backgroundColor": "lightgrey",
                    "color": "black",
                }},
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=52.1935,
                longitude=5.1173,
                zoom=7,
                pitch=35,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_radius=1000,
                    get_fill_color=[255, 140, 0],
                    get_line_color=[0, 0, 0],
                    tooltip='linenumber',
                    pickable=True

                ),
            ],
        ))
        time.sleep(5)