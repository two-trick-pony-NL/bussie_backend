import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

with st.empty():
    while True:
        df = pd.pandas.read_json('http://localhost/API/V1/get_vehicles', orient='index')
        df = pd.DataFrame(df,columns=['linenumber','latitude', 'longitude'])
        st.map(df)
        time.sleep(5)