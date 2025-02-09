import pandas as pd
import streamlit as st
from PIL import Image
from io import BytesIO
import requests
from raceplotly.plots import barplot

st.set_page_config(page_title="Serie A")
from Funzioni import *

st.title("Serie A")

st.subheader("Database storico della Serie A a girone unico")

seas_list = sorted(set(storico['Stagione']),reverse=True) #lista stagioni uniche
stagione_curr=str(seas_list[0])  #stagione corrente

rpl, part = st.columns(2)
with rpl:
    bcr=barplot(df=clas_rbc,item_column='Squadra',value_column='Scudetti',time_column='Anno')
    rbc = bcr.plot(time_label='Anno', value_label='Scudetti', title='Scudetti vinti', frame_duration=1000)
    st.plotly_chart(rbc, use_container_width=True)
with part:
    st.text('Partecipazioni Serie A')
    riep_part=pd.DataFrame({'Stagioni':list(storico['Stagione'])+list(storico['Stagione']),'Squadre':list(storico['CASA'])+list(storico['TRAS'])})
    riep_part=riep_part.drop_duplicates()
    riep_part.groupby('Squadre',as_index=False).agg({'Stagioni':'count'})
    riep_part = riep_part.sort_values(by=['Stagioni'], ascending=False)
    st.bar_chart(riep_part,x='Squadre',y='Stagioni')

st.subheader('Albo d\'oro')
for i in range(0, len(albo), 10):
    cols = st.columns(10)
    for j, (_, row) in enumerate(albo.iloc[i:i + 10].iterrows()):
        with cols[j]:
            st.image(Image.open(BytesIO(requests.get(row['url_Stemma']).content)), caption=f"{row['Vincitore']} ({row['Stagione']})", use_container_width=True)

