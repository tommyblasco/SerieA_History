import streamlit as st
st.set_page_config(page_title="Serie A - All timw",layout='wide')
from Funzioni import *

perp = st.tabs(['Classifica perpetua'])

with perp:
    pclass=ranking(seas='All').drop('Rk',axis=1)
    st.dataframe(pclass, hide_index=True)