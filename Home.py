import streamlit as st
st.set_page_config(page_title="Serie A",layout='wide')

import requests
from PIL import Image
from io import BytesIO
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from sqlalchemy import create_engine, text

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

with st.expander("Updates partite"):
    st.text("Info generali")
    col1, col2, col3 = st.columns(3)
    new_stag=col1.text_input("Stagione")
    new_data=col2.date_input("Data")
    new_gio=col3.number_input("Giornata",min_value=1,max_value=38,step=1)

    st.text("Partita")
    col4, col5 = st.columns(2)
    curr_seas_match = all_matches[all_matches['Stagione'] == new_stag]
    check1g = len(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS'])))
    with col4:
        if check1g != 20:
            new_ht = st.text_input("Squadra casa")
            new_allh = st.text_input("Allenatore casa")
        else:
            new_ht = st.selectbox('Squadra casa',
                                  sorted(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS']))))
            last_allh = curr_seas_match[curr_seas_match['CASA'] == new_ht].tail(1)['All CASA'].item()
            new_allh = st.text_input("Allenatore casa", value=last_allh)
    with col5:
        if check1g != 20:
            new_at = st.text_input("Squadra trasferta")
            new_alla = st.text_input("Allenatore trasferta")
        else:
            new_at = st.selectbox('Squadra trasferta',
                                  sorted(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS']))))
            last_alla = curr_seas_match[curr_seas_match['TRAS'] == new_at].tail(1)['All TRAS'].item()
            new_alla = st.text_input("Allenatore trasferta", value=last_alla)

    with st.form("Risultato"):
        st.subheader("Risultato")
        col6, col7 = st.columns(2)
        new_golh = col6.number_input(f"Gol {new_ht}",min_value=0,step=1,key='home_goal')
        new_gola = col7.number_input(f"Gol {new_at}",min_value=0,step=1,key='away_goal')
        id_match=new_stag[:4]+new_stag[5:7]+str(new_gio).zfill(2)+new_ht[:3]+new_at[:3]
        st.text(f"ID partita: {id_match}")
        submit_button = st.form_submit_button("Salva")

    if submit_button:
        try:
            with create_engine(st.secrets["DATABASE_URL"]).connect() as conn:
                query = text("""
                        INSERT INTO "Partite" ("ID", "Stagione", "Giornata", "Data", "CASA", "TRAS", "GC", "GT", "All CASA", "All TRAS")
                        VALUES (:id, :stag, :gio, :data, :casa, :tras, :gc, :gt, :all_casa, :all_tras)
                    """)
                conn.execute(query, {
                        "id": id_match,
                        "stag": new_stag,
                        "gio": new_gio,
                        "data": new_data,
                        "casa": new_ht,
                        "tras": new_at,
                        "gc":new_golh,
                        "gt":new_gola,
                        "all_casa":new_allh,
                        "all_tras":new_alla
                    })
                conn.commit()
            st.success(f"✅ ID {id_match} aggiunto con successo!")
        except Exception as e:
            st.error(f"Errore durante il salvataggio: {e}")

with (st.expander("Updates marcatori")):
    st.text("Info generali")
    col1, col2, col3 = st.columns(3)
    mnew_stag = col1.text_input("Stagione",key='stag_marc')
    mnew_data = col2.date_input("Data")
    mnew_gio = col3.number_input("Giornata", min_value=1, max_value=38, step=1)

    st.text("Partita")
    col4, col5 = st.columns(2)
    mcurr_seas_match = all_matches[all_matches['Stagione'] == mnew_stag]
    mcheck1g = len(set(list(mcurr_seas_match['CASA']) + list(mcurr_seas_match['TRAS'])))
    with col4:
        if mcheck1g != 20:
            mnew_ht = st.text_input("Squadra casa",key='ht_marc')
        else:
            mnew_ht = st.selectbox('Squadra casa', sorted(set(list(mcurr_seas_match['CASA']) + list(mcurr_seas_match['TRAS']))))
    with col5:
        if check1g != 20:
            mnew_at = st.text_input("Squadra trasferta",key='away_marc')
        else:
            mnew_at = st.selectbox('Squadra trasferta', sorted(set(list(mcurr_seas_match['CASA']) + list(mcurr_seas_match['TRAS']))))

    with st.form("Marcatori"):
        st.subheader("Marcatori")
        col6, col7, col8, col9 = st.columns(4)
        last20ysco=scorers[scorers['ID'].str[:4].astype(int)>=int(mnew_stag[:4])-20]
        last_id = max(scorers['id_marc'])
        with col6:
            st.text('Marcatore')
            scor1 = st.selectbox("Seleziona il marcatore:", ["➕ New Scorer"]+sorted(set(list(last20ysco['Marcatori'])+list(last20ysco['Assist']))))
            if scor1=="➕ New Scorer":
                new_scorer = st.text_input("Nuovo marcatore:")
            else:
                new_scorer=scor1
            st.text('Assist-man')
            ass1 = st.selectbox("Seleziona il marcatore:", ["➕ New Assistman","No Assist"]+sorted(set(list(last20ysco['Marcatori'])+list(last20ysco['Assist']))))
            if ass1=="➕ New Assistman":
                new_assist = st.text_input("Nuovo assistman:")
            elif ass1=="No Assist":
                new_assist=None
            else:
                new_assist=ass1
        with col7:
            st.text('Squadra')
            team_sco = st.selectbox("Seleziona la squadra:",[mnew_ht,mnew_at])
        min_sco = col8.number_input("Minuto",min_value=1,max_value=90,step=1,key='min_scor')
        with col9:
            min_rec_sco = st.number_input("Recupero",value=None,step=1,key='min_rec_scor')
            note=st.radio("Note",["R","A"],captions=['Rigore','Autogol'],index=None)
            note_sql = None if note is None else note

        mid_match=mnew_stag[:4]+mnew_stag[5:7]+str(mnew_gio).zfill(2)+mnew_ht[:3]+mnew_at[:3]
        submit_button_marc = st.form_submit_button("Salva")
        if submit_button_marc:
            try:
                with create_engine(st.secrets["DATABASE_URL"]).connect() as conn:
                    query = text("""
                            INSERT INTO "Marcatori" ("id_marc", "Marcatori", "Minuto", "Recupero", "Note", "Assist", "Squadra", "ID")
                            VALUES (:id_marc, :marcatore, :minuto, :recupero, :note, :assist, :squadra, :id)
                            """)
                    conn.execute(query, {
                        "id_marc": last_id+1,
                        "marcatore": new_scorer,
                        "minuto": min_sco,
                        "recupero": min_rec_sco,
                        "note": note_sql,
                        "assist": new_assist,
                        "squadra": team_sco,
                        "id": mid_match
                    })
                    conn.commit()
                st.success(f"✅ id_match n: {last_id+1}, ID: {mid_match} aggiunto con successo!")
            except Exception as e:
                st.error(f"Errore durante il salvataggio: {e}")