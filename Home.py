import streamlit as st
st.set_page_config(page_title="Serie A")
from Funzioni import *

st.title("Serie A")

st.subheader("Database storico della Serie A a girone unico")

seas_list = sorted(set(storico['Stagione']),reverse=True) #lista stagioni uniche
stagione_curr=str(seas_list[0])  #stagione corrente

gen_al=albo(seas_list) #generazione albo d'oro
for i in range(0, len(seas_list), 10):
    # Crea le colonne per la riga
    cols = st.columns(10)
    # Itera per le immagini nella riga corrente
    for j, (stagione, (squadra, img)) in enumerate(list(gen_al.items())[i:i + 10]):
        with cols[j]:
            st.image(Image.open(BytesIO(requests.get(img).content)), use_column_width=True)
            st.write(f"**{stagione}**")
            st.write(squadra)


#st.header("Stagione attuale "+stagione_curr)
#tm_delta=st.slider("Partite nei prossimi ... giorni",min_value=0,max_value=35,value=7,step=7)

#st.dataframe(nx_match_rank(s=stagione_curr,n=tm_delta))