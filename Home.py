import streamlit as st
st.set_page_config(page_title="Serie A")
from Funzioni import *

st.title("Serie A")

st.subheader("Database storico della Serie A a girone unico")

stagione_curr=str(max(set(storico['Stagione'])))
st.header("Stagione attuale "+stagione_curr)
tm_delta=st.slider("Partite nei prossimi ... giorni",min_value=0,max_value=35,value=7,step=7)

st.dataframe(nx_match_rank(s=stagione_curr,n=tm_delta))