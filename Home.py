import streamlit as st
st.set_page_config(page_title="Serie A",layout='wide')

import requests
from PIL import Image
from io import BytesIO
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np

st.title("Serie A")

st.subheader("Database storico della Serie A a girone unico")
st.markdown("*Tutti i risultati ed i marcatori dal 1929-30 ad oggi*")

st.image(Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_History/blob/main/images/varie/main.png?raw=True").content)), use_container_width=True)

st.write("Apri la barra laterale a sinistra e scopri le varie sezioni")
cd1, cd2, cd3, cd4 = st.columns(4)
with cd1:
    st.image(Image.open(BytesIO(requests.get(
        f"https://github.com/tommyblasco/SerieA_History/blob/main/images/varie/Stagioni.png?raw=True").content)),
            caption='Stagioni', use_container_width=True)
with cd2:
    st.image(Image.open(BytesIO(requests.get(
        f"https://github.com/tommyblasco/SerieA_History/blob/main/images/varie/Squadre.png?raw=True").content)),
            caption='Squadre', use_container_width=True)
with cd3:
    st.image(Image.open(BytesIO(requests.get(
        f"https://github.com/tommyblasco/SerieA_History/blob/main/images/varie/Precedenti.png?raw=True").content)),
            caption='Precedenti', use_container_width=True)
with cd4:
    st.image(Image.open(BytesIO(requests.get(
        f"https://github.com/tommyblasco/SerieA_History/blob/main/images/varie/Alltime.png?raw=True").content)),
            caption='All time', use_container_width=True)


def load_data(n):
    l_data = st.connection(n, type=GSheetsConnection)
    l_data1 = l_data.read(worksheet="Foglio1")
    return l_data1

if "storico" not in st.session_state:
    st.session_state.storico = load_data(n="gspartite")

if "marcatori" not in st.session_state:
    st.session_state.marcatori = load_data(n="gsmarcatori")

if st.button("Aggiorna Dati"):
    st.session_state.storico = load_data(n="gspartite")
    st.session_state.marcatori = load_data(n="gsmarcatori")

storico=st.session_state.storico.copy()
marcatori=st.session_state.marcatori.copy()

storico['Data']=pd.to_datetime(storico['Data'], dayfirst=True)
storico['Giorno'] = storico['Data'].dt.strftime('%b %d, %Y')
storico['Data']=[x.date() for x in storico['Data']]
#storico['GC']=[int(x) for x in storico['GC']]
#storico['GT']=[int(x) for x in storico['GT']]
marcatori=marcatori[~marcatori['Minuto'].isna()]
marcatori['Minuto']=[int(x) for x in marcatori['Minuto']]
marcatori['Recupero']=[int(x) if not pd.isna(x) else np.nan for x in marcatori['Recupero'] ]
marcatori['Recupero'] = marcatori['Recupero'].astype('Int64')

