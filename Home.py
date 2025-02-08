import pandas as pd
import streamlit as st
from PIL import Image
from io import BytesIO
import requests

st.set_page_config(page_title="Serie A")
from Funzioni import *

st.title("Serie A")

st.subheader("Database storico della Serie A a girone unico")

seas_list = sorted(set(storico['Stagione']),reverse=True) #lista stagioni uniche
stagione_curr=str(seas_list[0])  #stagione corrente

for i in range(0, len(albo), 10):
    cols = st.columns(10)
    for j, (_, row) in enumerate(albo.iloc[i:i + 10].iterrows()):
        with cols[j]:
            st.image(Image.open(BytesIO(requests.get(row['url_Stemma']).content)), caption=f"{row['Vincitore']} ({row['Stagione']})", use_container_width=True)

#st.header("Stagione attuale "+stagione_curr)
#tm_delta=st.slider("Partite nei prossimi ... giorni",min_value=0,max_value=35,value=7,step=7)

#st.dataframe(nx_match_rank(s=stagione_curr,n=tm_delta))