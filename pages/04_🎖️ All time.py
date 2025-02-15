import streamlit as st
st.set_page_config(page_title="Serie A - All timw",layout='wide')
from Funzioni import *

perp, rec = st.tabs(['Classifica perpetua','Record'])

with perp:
    pclass=ranking(seas='All').drop('Rk',axis=1)
    st.dataframe(pclass, hide_index=True)