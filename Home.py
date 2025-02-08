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

gen_al=albo(seas_list) #generazione albo d'oro
st.dataframe(pd.DataFrame.from_dict(gen_al, orient='index', columns=["Vincitore", "url_Stemma"]).reset_index(drop=True, inplace=True))


#st.header("Stagione attuale "+stagione_curr)
#tm_delta=st.slider("Partite nei prossimi ... giorni",min_value=0,max_value=35,value=7,step=7)

#st.dataframe(nx_match_rank(s=stagione_curr,n=tm_delta))