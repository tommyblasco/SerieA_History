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
            lista_all=[x if z==new_ht else y if aa==new_ht else '' for x,y,z,aa in zip(curr_seas_match['All CASA'],curr_seas_match['All TRAS'],curr_seas_match['CASA'],curr_seas_match['TRAS'])]
            last_allh = [x for x in lista_all if x!=''][-1]
            new_allh = st.text_input("Allenatore casa", value=last_allh)
    with col5:
        if check1g != 20:
            new_at = st.text_input("Squadra trasferta")
            new_alla = st.text_input("Allenatore trasferta")
        else:
            new_at = st.selectbox('Squadra trasferta',
                                  sorted(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS']))))
            lista_all=[x if z==new_at else y if aa==new_at else '' for x,y,z,aa in zip(curr_seas_match['All CASA'],curr_seas_match['All TRAS'],curr_seas_match['CASA'],curr_seas_match['TRAS'])]
            last_alla = [x for x in lista_all if x!=''][-1]
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
            new_ht = st.text_input("Squadra casa",key='new_ht1')
        else:
            new_ht = st.selectbox('Squadra casa',sorted(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS']))),key='new_ht1')
    with col5:
        if check1g != lega_gg[new_league_eu]:
            new_at = st.text_input("Squadra trasferta",key='new_at1')
        else:
            new_at = st.selectbox('Squadra trasferta', sorted(set(list(curr_seas_match['CASA']) + list(curr_seas_match['TRAS']))),key='new_at1')

    with st.form("Risultato Campionati Europei"):
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

st.subheader("Coppe Europei")
with st.expander("Updates Partite"):
    st.text("Info generali")
    col1, col2 = st.columns(2)
    with col1:
        new_league_ceu=st.selectbox("Seleziona la coppa:",['Champions League','Europa League','Conference League'],key='sel_cup')
        new_stag_ceu=st.text_input("Stagione",key='new_s2')
        new_data_ceu=st.date_input("Data",key='new_date2')
    db_coppe = {'Champions League': champions, 'Europa League': eu_league, 'Conference League': conf_league}
   # curr_seas_match = db_coppe[new_league_ceu][db_coppe[new_league_ceu]['Stagione'] == new_stag_ceu]
    coppe_table = {'Champions League': 'ChampionsLeague', 'Europa League': 'EuropaLeague', 'Conference League': 'ConferenceLeague'}
    with col2:
        new_fase1=st.selectbox("Fase 1",sorted(set(list(db_coppe[new_league_ceu]['Fase_1']))),key='fase1')
        new_fase2 = st.selectbox("Fase 2", sorted(set(list(db_coppe[new_league_ceu]['Fase_2']))), key='fase2')
        new_fase3 = st.selectbox("And/Rit", sorted(set(list(db_coppe[new_league_ceu]['Fase_3']))), key='fase3')

    st.text("Partita")
    col3, col4, col5, col6 = st.columns([3,1,3,1])
    with col3:
        ht_select = st.selectbox('Squadra casa',sorted(set(list(db_coppe[new_league_ceu]['CASA']) + list(db_coppe[new_league_ceu]['TRAS']))),key='sel_ht')
        ht_new = st.text_input("Inserisci nuova squadra", key='new_ht2')
        ht_final = ht_select if ht_new=='' else ht_new
    naz_ht = col4.text_input("Nazione casa",key='naz_casa')
    with col5:
        at_select = st.selectbox('Squadra trasferta',sorted(set(list(db_coppe[new_league_ceu]['CASA']) + list(db_coppe[new_league_ceu]['TRAS']))),key='sel_at')
        at_new = st.text_input("Inserisci nuova squadra", key='new_at2')
        at_final = at_select if at_new=='' else at_new
    naz_at = col6.text_input("Nazione tras",key='naz_tras')

    with st.form("Risultato Coppe"):
        st.subheader("Risultato")
        col7, col8, col9, col10, col11, col12 = st.columns([2,2,1,1,1,1])
        new_golh = col7.number_input(f"Gol al 90 {new_ht}",min_value=0,step=1,key='home_goal2')
        new_gola = col8.number_input(f"Gol al 90 {new_at}",min_value=0,step=1,key='away_goal2')
        new_sup_golh = col9.number_input(f"Supp {new_ht}",value=None,step=1,key='sup_home_goal')
        new_sup_gola = col10.number_input(f"Supp {new_at}",value=None,step=1,key='sup_away_goal')
        new_rig_golh = col11.number_input(f"Rigori {new_ht}",value=None,step=1,key='rig_home_goal')
        new_rig_gola = col12.number_input(f"Rigori {new_at}",value=None,step=1,key='rig_away_goal')
        submit_button = st.form_submit_button("Salva")

    if submit_button:
        try:
            with create_engine(st.secrets["DATABASE1_URL"]).connect() as conn:
                query = text(f"""
                        INSERT INTO "{coppe_table[new_league_ceu]}" ("Stagione", "Fase_1", "Fase_2", "Fase_3", "Data", "CASA", "NazC" "TRAS", "NazT", "GC", "GT", "GCS", "GTS", "RigC","RigT")
                        VALUES (:stag, :f1,:f2,:f3, :data, :casa, :nazc, :tras, :nazt, :gc, :gt, :gcs, :gts, :rigc, :rigt)
                    """)
                conn.execute(query, {
                        "stag": new_stag_ceu,
                        "f1": new_fase1, "f2": new_fase2, "f3": new_fase3,
                        "casa":ht_final, "nazc":naz_ht, "tras": at_final, "nazt":naz_at,
                        "gc":new_golh, "gt":new_gola,
                        "gcs": new_sup_golh, "gts": new_sup_gola,
                    "rigc": new_rig_golh, "rigt": new_rig_gola
                    })
                conn.commit()
            st.success(f"✅ {new_ht}-{new_at} aggiunto con successo!")
        except Exception as e:
            st.error(f"Errore durante il salvataggio: {e}")