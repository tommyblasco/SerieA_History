import streamlit as st
st.set_page_config(page_title="Serie A",layout='wide')

import requests
from PIL import Image
from io import BytesIO
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from sqlalchemy import create_engine

st.title("Serie A")

st.subheader("Database storico della Serie A a girone unico")
st.markdown("*Tutti i risultati ed i marcatori dal 1929-30 ad oggi*")

@st.cache_data
def load_images_varie(img):
    return Image.open(BytesIO(requests.get(f"https://github.com/tommyblasco/SerieA_History/blob/main/images/varie/{img}.png?raw=True").content))


st.image(load_images_varie(img='main'), use_container_width=True)

st.write("Apri la barra laterale a sinistra e scopri le varie sezioni")
cd1, cd2, cd3, cd4 = st.columns(4)
with cd1:
    st.image(load_images_varie(img='Stagioni'),
            caption='Stagioni', use_container_width=True)
with cd2:
    st.image(load_images_varie(img='Squadre'),
            caption='Squadre', use_container_width=True)
with cd3:
    st.image(load_images_varie(img='Precedenti'),
            caption='Precedenti', use_container_width=True)
with cd4:
    st.image(load_images_varie(img='Alltime'),
            caption='All time', use_container_width=True)

@st.cache_data
def load_data(n, eng):
    #l_data = st.connection(n, type=GSheetsConnection)
    #l_data1 = l_data.read(worksheet="Foglio1")
    #return l_data1
    engine=create_engine(st.secrets[eng])
    return pd.read_sql(f"SELECT * FROM {n}", engine)

if "storico" not in st.session_state:
    #st.session_state.storico = load_data(n="gspartite")
    st.session_state.storico = load_data(n='"Partite"',eng="DATABASE_URL")

if "marcatori" not in st.session_state:
    #st.session_state.marcatori = load_data(n="gsmarcatori")
    st.session_state.marcatori = load_data(n='"Marcatori"',eng="DATABASE_URL")

if "premierleague" not in st.session_state:
    st.session_state.premierleague = load_data(n='"PremierLeague"',eng="DATABASE1_URL")
if "laliga" not in st.session_state:
    st.session_state.laliga = load_data(n='"LaLiga"',eng="DATABASE1_URL")
if "ligue1" not in st.session_state:
    st.session_state.ligue1 = load_data(n='"Ligue1"',eng="DATABASE1_URL")
if "bundesliga" not in st.session_state:
    st.session_state.bundesliga = load_data(n='"Bundesliga"',eng="DATABASE1_URL")
if "champions" not in st.session_state:
    st.session_state.champions = load_data(n='"ChampionsLeague"',eng="DATABASE1_URL")
if "euleague" not in st.session_state:
    st.session_state.euleague = load_data(n='"EuropaLeague"',eng="DATABASE1_URL")
if "confleague" not in st.session_state:
    st.session_state.confleague = load_data(n='"ConferenceLeague"',eng="DATABASE1_URL")


if st.button("🔄 Aggiorna Serie A"):
    with st.spinner("🔃 Aggiornamento Serie A..."):
        st.cache_data.clear()
        st.session_state.storico = load_data(n='"Partite"',eng="DATABASE_URL")
        st.session_state.marcatori = load_data(n='"Marcatori"',eng="DATABASE_URL")

if st.button("🔄 Aggiorna Camp Europei"):
    with st.spinner("🔃 Aggiornamento Campionati Europei..."):
        st.cache_data.clear()  # 🔥 Forza il ricaricamento della cache
        st.session_state.premierleague = load_data(n='"PremierLeague"',eng="DATABASE1_URL")
        st.session_state.laliga = load_data(n='"LaLiga"',eng="DATABASE1_URL")
        st.session_state.bundesliga = load_data(n='"Bundesliga"', eng="DATABASE1_URL")
        st.session_state.ligue1 = load_data(n='"Ligue1"', eng="DATABASE1_URL")

if st.button("🔄 Aggiorna Coppe Europee"):
    with st.spinner("🔃 Aggiornamento Coppe Europee..."):
        st.cache_data.clear()
        st.session_state.champions = load_data(n='"ChampionsLeague"', eng="DATABASE1_URL")
        st.session_state.euleague = load_data(n='"EuropaLeague"', eng="DATABASE1_URL")
        st.session_state.confleague = load_data(n='"ConferenceLeague"', eng="DATABASE1_URL")

