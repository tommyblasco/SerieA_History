import streamlit as st
st.set_page_config(page_title="Serie A - All time",layout='wide')
from Funzioni import *

perp, rec = st.tabs(['Classifica perpetua','Record'])

with perp:
    st.subheader('Classifica perpetua')
    pclass=ranking(seas='All').drop('Rk',axis=1)
    st.dataframe(pclass, hide_index=True)

    with st.expander('Media gol stagionale'):
        storico['Gol Tot']=[x+y for x,y in zip(storico['GC'],storico['GT'])]
        dfg=storico.groupby('Stagione',as_index=False).agg({'Gol Tot':'mean'})
        df_gr = px.line(dfg, x="Stagione", y="Gol Tot", markers=True)
        df_gr.update_layout(xaxis=dict(title="Stagione", type="category"),yaxis=dict(title="Media Gol"))
        st.plotly_chart(df_gr)
    with st.expander('Vittorie C/T stagionale'):
        storico['WH']=[100 if x>y else 0 for x,y in zip(storico['GC'],storico['GT'])]
        storico['WA'] = [100 if x < y else 0 for x, y in zip(storico['GC'], storico['GT'])]
        storico['N'] = [100 if x == y else 0 for x, y in zip(storico['GC'], storico['GT'])]
        dfg1 = storico.groupby('Stagione', as_index=False).agg({'WH': 'mean','WA':'mean','N':'mean'})
        dfg1_gr = px.bar(dfg1, x="Stagione", y=['WH','N','WA'])
        dfg1_gr.update_layout(xaxis=dict(title="Stagione", type="category"),yaxis=dict(title="% W H/A"))
        st.plotly_chart(dfg1_gr)

