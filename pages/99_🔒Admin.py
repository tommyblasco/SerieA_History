import streamlit as st
from Funzioni import *
from sqlalchemy import create_engine, text

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Admin – Data Entry", page_icon="🔒", layout="centered")
# ---------------------------
# AUTH
# ---------------------------
def check_password():
    """Ritorna True se password corretta"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    with st.form("login_form"):
        st.subheader("🔒 Area riservata")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Accedi")

    if submit:
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.authenticated = True
            st.success("Accesso consentito")
            st.rerun()
    else:
        st.error("Password errata")

    return False

if not check_password():
    st.stop()

# ---------------------------
# ADMIN PAGE
# ---------------------------
st.title("🛠️ Admin – Data Entry")
st.info("Qui puoi aggiornare i dati dell'applicazione.")

#refresho
scorers = st.session_state.marcatori.copy()
seriea = st.session_state.storico.copy()
premierleague = st.session_state.premierleague.copy()
laliga = st.session_state.laliga.copy()
ligue1 = st.session_state.ligue1.copy()
bundesliga = st.session_state.bundesliga.copy()
champions = st.session_state.champions.copy()
eu_league = st.session_state.euleague.copy()
conf_league = st.session_state.confleague.copy()

st.subheader("Serie A")
with st.expander("Updates Partite"):
    st.text("Info generali")
    col1, col2, col3 = st.columns(3)
    new_stag=col1.text_input("Stagione")
    new_data=col2.date_input("Data")
    new_gio=col3.number_input("Giornata",min_value=1,max_value=38,step=1)

    st.text("Partita")
    col4, col5 = st.columns(2)
    curr_seas_match = seriea[seriea['Stagione'] == new_stag]
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
    col1, col2 = st.columns(2)
    mnew_stag = col1.text_input("Stagione",key='stag_marc',value="0000/00")
    mnew_gio = col2.number_input("Giornata", min_value=1, max_value=38, step=1,key='gio_marc')

    st.text("Partita")
    col4, col5 = st.columns(2)
    mcurr_seas_match = seriea[seriea['Stagione'] == mnew_stag]
    mcheck1g = len(set(list(mcurr_seas_match['CASA']) + list(mcurr_seas_match['TRAS'])))
    with col4:
        if mcheck1g != 20:
            mnew_ht = st.text_input("Squadra casa",key='ht_marc')
        else:
            mnew_ht = st.selectbox('Squadra casa', sorted(set(list(mcurr_seas_match['CASA']) + list(mcurr_seas_match['TRAS']))),key='ht_marc')
    with col5:
        if mcheck1g != 20:
            mnew_at = st.text_input("Squadra trasferta",key='away_marc')
        else:
            mnew_at = st.selectbox('Squadra trasferta', sorted(set(list(mcurr_seas_match['CASA']) + list(mcurr_seas_match['TRAS']))),key='away_marc')

    with st.form("Marcatori"):
        st.subheader("Marcatori")
        col6, col7, col8, col9 = st.columns(4)
        last20ysco=scorers[scorers['ID'].str[:4].astype(int)>=int(mnew_stag[:4])-20]
        assist_list=[x for x in last20ysco['Assist'] if x is not None]
        marc_list = [x for x in last20ysco['Marcatori'] if x is not None]
        with col6:
            scor1 = st.selectbox("Seleziona il marcatore:", sorted(set(marc_list+assist_list)),key='marc_form')
            new_scorer = st.text_input("Nuovo marcatore:", key='marc_form1')
            final_scorer = scor1 if new_scorer=='' else new_scorer

            st.text('Assist-man')
            ass1 = st.selectbox("Seleziona l'assistman:", ["No Assist"]+sorted(set(marc_list+assist_list)),key='ass_form')
            new_assist = st.text_input("Nuovo assistman:", key='ass_form1')
            if ass1=="No Assist":
                final_assist = None
            elif new_assist=="":
                final_assist=ass1
            else:
                final_assist=new_assist
        team_sco = col7.selectbox("Seleziona la squadra:",[mnew_ht,mnew_at],key='team_form')
        min_sco = col8.number_input("Minuto",min_value=1,max_value=90,step=1,key='min_scor')
        with col9:
            min_rec_sco = st.number_input("Recupero",value=None,step=1,key='min_rec_scor')
            note=st.radio("Note",["R","A","0"],captions=['Rigore','Autogol','None'],index=None,key='radio_form')
            note_sql = None if note is None or note=="0" else note

        mid_match=mnew_stag[:4]+mnew_stag[5:7]+str(mnew_gio).zfill(2)+mnew_ht[:3]+mnew_at[:3]
        submit_button_marc = st.form_submit_button("Salva")
        if submit_button_marc:
            try:
                with create_engine(st.secrets["DATABASE_URL"]).connect() as conn:
                    query = text("""
                            INSERT INTO "Marcatori" ("Marcatori", "Minuto", "Recupero", "Note", "Assist", "Squadra", "ID")
                            VALUES (:marcatore, :minuto, :recupero, :note, :assist, :squadra, :id)
                            """)
                    conn.execute(query, {
                        "marcatore": final_scorer,
                        "minuto": min_sco,
                        "recupero": min_rec_sco,
                        "note": note_sql,
                        "assist": final_assist,
                        "squadra": team_sco,
                        "id": mid_match
                    })
                    conn.commit()
                st.success(f"✅ {final_scorer} at {str(min_sco)} aggiunto con successo!")
            except Exception as e:
                st.error(f"Errore durante il salvataggio: {e}")


st.subheader("Campionati Europei")
with st.expander("Updates Partite"):
    st.text("Info generali")
    col1, col2, col3, col4 = st.columns(4)
    new_league_eu=col1.selectbox("Seleziona la lega:",['Premier League','La Liga','Bundesliga','Ligue 1'])
    new_stag_eu=col2.text_input("Stagione",key='new_s1')
    new_data_eu=col3.date_input("Data",key='new_date1')
    new_gio_eu=col4.number_input("Giornata",min_value=1,max_value=38,step=1,key='new_gio1')

    st.text("Partita")
    col4, col5 = st.columns(2)
    db_lega = {'Premier League':premierleague,'La Liga':laliga,'Bundesliga':bundesliga,'Ligue 1':ligue1}
    lega_gg = {'Premier League': 20, 'La Liga': 20, 'Bundesliga': 18, 'Ligue 1': 18}
    lega_table = {'Premier League': 'PremierLeague', 'La Liga': 'LaLiga', 'Bundesliga': 'Bundesliga', 'Ligue 1': 'Ligue1'}
    curr_seas_match = db_lega[new_league_eu][db_lega[new_league_eu]['Stagione'] == new_stag_eu]
    check1g = len(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS'])))
    with col4:
        if check1g != lega_gg[new_league_eu]:
            new_ht = st.text_input("Squadra casa")
        else:
            new_ht = st.selectbox('Squadra casa',sorted(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS']))))
    with col5:
        if check1g != lega_gg[new_league_eu]:
            new_at = st.text_input("Squadra trasferta")
        else:
            new_at = st.selectbox('Squadra trasferta', sorted(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS']))))

    with st.form("Risultato"):
        st.subheader("Risultato")
        col6, col7 = st.columns(2)
        new_golh = col6.number_input(f"Gol {new_ht}",min_value=0,step=1,key='home_goal1')
        new_gola = col7.number_input(f"Gol {new_at}",min_value=0,step=1,key='away_goal1')
        submit_button = st.form_submit_button("Salva")

    if submit_button:
        try:
            with create_engine(st.secrets["DATABASE1_URL"]).connect() as conn:
                query = text(f"""
                        INSERT INTO "{lega_table[new_league_eu]}" ("Stagione", "Giornata", "Data", "CASA", "TRAS", "GC", "GT")
                        VALUES (:stag, :gio, :data, :casa, :tras, :gc, :gt)
                    """)
                conn.execute(query, {
                        "stag": new_stag_eu,
                        "gio": new_gio_eu,
                        "data": new_data_eu,
                        "casa": new_ht,
                        "tras": new_at,
                        "gc":new_golh,
                        "gt":new_gola
                    })
                conn.commit()
            st.success(f"✅ {new_ht}-{new_at} aggiunto con successo!")
        except Exception as e:
            st.error(f"Errore durante il salvataggio: {e}")