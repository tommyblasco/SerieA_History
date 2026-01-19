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


def load_data(n):
    #l_data = st.connection(n, type=GSheetsConnection)
    #l_data1 = l_data.read(worksheet="Foglio1")
    #return l_data1
    engine=create_engine(st.secrets["DATABASE_URL"])
    return pd.read_sql(f"SELECT * FROM {n}", engine)

if "storico" not in st.session_state:
    #st.session_state.storico = load_data(n="gspartite")
    st.session_state.storico = load_data(n='"Partite"')

if "marcatori" not in st.session_state:
    #st.session_state.marcatori = load_data(n="gsmarcatori")
    st.session_state.marcatori = load_data(n='"Marcatori"')

if st.button("🔄 Aggiorna Dati"):
    with st.spinner("🔃 Aggiornamento in corso..."):
        st.cache_data.clear()  # 🔥 Forza il ricaricamento della cache
        #st.session_state.storico = load_data(n="gspartite")
        #st.session_state.marcatori = load_data(n="gsmarcatori")

        st.session_state.storico = load_data(n='"Partite"')
        st.session_state.marcatori = load_data(n='"Marcatori"')


scorers = st.session_state.marcatori.copy()
all_matches = st.session_state.storico.copy()

with st.form("Inserisci nuove partite"):
    st.text("Info generali")
    col1, col2, col3 = st.columns(3)
    new_stag=col1.text_input("Stagione")
    new_data=col2.date_input("Data")
    new_gio=col3.number_input("Giornata",min_value=1,max_value=38,step=1)
    st.text("Partita")
    col4, col5 = st.columns(2)
    curr_seas_match = all_matches[all_matches['Stagione'] == new_stag]
    check1g=len(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS'])))
    with col4:
        if check1g!=20:
            new_ht=st.text_input("Squadra casa")
            new_allh=st.text_input("Allenatore casa")
        else:
            new_ht=st.selectbox('Squadra casa', sorted(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS']))))
            last_allh=curr_seas_match[curr_seas_match['CASA']==new_ht].tail(1)['All CASA']
            new_allh = st.text_input("Allenatore casa", value=last_allh)
        new_golh = st.number_input("Gol",min_value=0,step=1)
    with col5:
        if check1g!=20:
            new_at=st.text_input("Squadra trasferta")
            new_alla=st.text_input("Allenatore trasferta")
        else:
            new_at=st.selectbox('Squadra trasferta', sorted(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS']))))
            last_alla=curr_seas_match[curr_seas_match['TRAS']==new_at].tail(1)['All TRAS']
            new_alla = st.text_input("Allenatore trasferta", value=last_alla)
        new_gola = st.number_input("Gol",min_value=0,step=1)

        submit_button = st.form_submit_button("Salva")