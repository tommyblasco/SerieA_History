import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import streamlit as st
from github import Github
import base64
from streamlit_gsheets import GSheetsConnection
from PIL import Image
from io import BytesIO
import requests
from raceplotly.plots import barplot
import plotly.graph_objects as go
import plotly.express as px


conn_g=Github(st.secrets['TOKEN'])
repo_seriea=conn_g.get_user("tommyblasco").get_repo("SerieA_History")


@st.cache_data
def load_images(team,yyyy):
    stemmi_ava=repo_seriea.get_contents(f"/images/stemmi/{team}")
    file_names = [file.name.split(".")[0] for file in stemmi_ava]
    yy_sel=min([x for x in file_names if x>=yyyy])
    url_stemma=f"https://github.com/tommyblasco/SerieA_History/blob/main/images/stemmi/{team}/{yy_sel}.png?raw=True".replace(' ','%20')
    return url_stemma

def get_storico():
    if "storico" in st.session_state:
        storico = st.session_state.storico.copy()
        storico['Data'] = pd.to_datetime(storico['Data'], dayfirst=True)
        storico['Giorno'] = storico['Data'].dt.strftime('%b %d, %Y')
        storico['Data'] = storico['Data'].dt.date
        return storico
    else:
        return None

def get_marcatori():
    if "marcatori" in st.session_state:
        marcatori = st.session_state.marcatori.copy()
        marcatori = marcatori[~marcatori['Minuto'].isna()]
        marcatori['Minuto'] = marcatori['Minuto'].astype(int)
        marcatori['Recupero'] = marcatori['Recupero'].apply(lambda x: int(x) if not pd.isna(x) else np.nan)
        marcatori['Recupero'] = marcatori['Recupero'].astype('Int64')
        return marcatori
    else:
        return None


penalita=pd.read_csv(f"https://raw.githubusercontent.com/tommyblasco/SerieA_History/refs/heads/main/Dati/Penalizzazioni.csv",
                             sep=",", decimal=".", parse_dates=['Da','A'],dayfirst=True)
albo=pd.read_csv('https://raw.githubusercontent.com/tommyblasco/SerieA_History/refs/heads/main/Dati/albo_doro.csv',sep=";",decimal='.')
clas_rbc=pd.read_csv('https://raw.githubusercontent.com/tommyblasco/SerieA_History/refs/heads/main/Dati/albo_cum.csv',sep=";",decimal='.')
colori_team=pd.read_csv('https://raw.githubusercontent.com/tommyblasco/SerieA_History/refs/heads/main/Dati/Colors.csv',sep=";",decimal='.')

penalita['Da']=[x.date() for x in penalita['Da']]
penalita['A']=[x.date() for x in penalita['A']]

#classifica x tutte le stagioni

def ranking(dati,seas,st_date=date(1900,1,1),en_date=date.today()):
    if seas=='All':
        db=dati
    else:
        db=dati[(dati['Stagione']==seas) & (dati['Data']>=st_date) & (dati['Data']<=en_date)]
    db['H']=[1 if x>y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['N']=[1 if x==y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['A']=[1 if x<y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['PH']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['H'],db['N'],db['Stagione'])]
    db['PA']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['A'],db['N'],db['Stagione'])]
    casa=db.groupby(['CASA'],as_index=False).agg({'PH':'sum','Data':'count','H':'sum','N':'sum','A':'sum','GC':'sum','GT':'sum'})
    trasferta=db.groupby(['TRAS'],as_index=False).agg({'PA':'sum','Data':'count','A':'sum','N':'sum','H':'sum','GT':'sum','GC':'sum'})
    casa['DRC']=[x-y for x,y in zip(casa['GC'],casa['GT'])]
    trasferta['DRT']=[x-y for x,y in zip(trasferta['GT'],trasferta['GC'])]
    casa.columns=['Squadra','Punti','Gio','V','N','P','GF','GS','DR']
    trasferta.columns=['Squadra','Punti','Gio','V','N','P','GF','GS','DR']
    classifica=pd.concat([casa,trasferta],ignore_index=True).groupby(['Squadra'],as_index=False).agg({'Punti':'sum','Gio':'sum','V':'sum','N':'sum','P':'sum','GF':'sum','GS':'sum','DR':'sum'})
    if seas!='All':
        if en_date==date.today():
            pen_date=max(db['Data'])
        else:
            pen_date=en_date
        pen_fil=penalita[(penalita['Stagione']==seas) & (penalita['Da']<=pen_date) & (penalita['A']>=pen_date)]
        if pen_fil.shape[0]>0:
            new_class = classifica.merge(pen_fil[['Squadra','Pen']], on='Squadra',how='left')
            new_class['Pnt']=[int(x-y) if not np.isnan(y) else int(x) for x,y in zip(new_class['Punti'],new_class['Pen'])]
            new_class=new_class[['Squadra','Pnt','Gio','V','N','P','GF','GS','DR']]
            new_class = new_class.sort_values(by=['Pnt', 'DR'], ascending=False)
        else:
            new_class=classifica.sort_values(by=['Punti', 'DR'], ascending=False)
    else:
        new_class=classifica[['Squadra','Gio','V','N','P','GF','GS']]
        new_class.insert(1,"Med Pnt 3W",[round((x*3+y)/z,3) for x,y,z in zip(new_class['V'],new_class['N'],new_class['Gio'])])
        new_class = new_class.sort_values(by=['Med Pnt 3W'], ascending=False)
    new_class.insert(0,'Rk',range(1,new_class.shape[0]+1))
    return new_class

#prossima giornata avendo anche il rif alla posizione della squadra
def class_cum(dati,seas):
    db = dati[(dati['Stagione'] == seas)]
    db['H']=[1 if x>y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['N']=[1 if x==y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['A']=[1 if x<y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['PH']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['H'],db['N'],db['Stagione'])]
    db['PA']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['A'],db['N'],db['Stagione'])]
    new_db_l=pd.DataFrame({'Squadra':list(db['CASA'])+list(db['TRAS']),'Giornata':list(db['Giornata'])+list(db['Giornata']),'Punti':list(db['PH'])+list(db['PA'])})
    new_db_l = new_db_l.sort_values(by=['Giornata'])
    new_db_l['CumP'] = new_db_l.groupby(['Squadra'], as_index=False)['Punti'].transform(pd.Series.cumsum)
    return new_db_l

def class_ct(dati,seas):
    db = dati[(dati['Stagione'] == seas)]
    db['H']=[1 if x>y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['N']=[1 if x==y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['A']=[1 if x<y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['PH']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['H'],db['N'],db['Stagione'])]
    db['PA']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['A'],db['N'],db['Stagione'])]
    casa=db.groupby(['CASA'],as_index=False).agg({'PH':'sum','Data':'count','H':'sum','N':'sum','A':'sum','GC':'sum','GT':'sum'})
    trasferta=db.groupby(['TRAS'],as_index=False).agg({'PA':'sum','Data':'count','A':'sum','N':'sum','H':'sum','GT':'sum','GC':'sum'})
    casa['DRC']=[x-y for x,y in zip(casa['GC'],casa['GT'])]
    trasferta['DRT']=[x-y for x,y in zip(trasferta['GT'],trasferta['GC'])]
    casa.columns=['Squadra','Punti','Gio','V','N','P','GF','GS','DR']
    trasferta.columns=['Squadra','Punti','Gio','V','N','P','GF','GS','DR']
    casa = casa.sort_values(by=['Punti','DR'], ascending=False)
    trasferta = trasferta.sort_values(by=['Punti', 'DR'], ascending=False)
    return [casa, trasferta]

def mister_alltime(dati):
    dati_pt2 = dati[['ID','Stagione','Giornata','Data','TRAS','CASA','GT','GC','All TRAS','All CASA']]
    dati=dati[['ID','Stagione','Giornata','Data','CASA','TRAS','GC','GT','All CASA','All TRAS']]
    dati.columns=['ID','Stagione','Giornata','Data','Squadra','Opponent','GF','GS','Allenatore','All opponent']
    dati_pt2.columns = ['ID', 'Stagione', 'Giornata', 'Data', 'Squadra', 'Opponent', 'GF', 'GS', 'Allenatore',
                    'All opponent']
    db=pd.concat([dati,dati_pt2])
    db['W'] = [1 if x > y else 0 for x, y in zip(db['GF'], db['GS'])]
    db['N'] = [1 if x == y else 0 for x, y in zip(db['GF'], db['GS'])]
    db['L'] = [1 if x < y else 0 for x, y in zip(db['GF'], db['GS'])]
    db['Pnt'] = [x * 3 + y  for x, y in zip(db['W'], db['N'])]
    mrallt=db.groupby(['Allenatore'],as_index=False).agg({'Pnt':'mean','Squadra':list,'Data':'count','W':'sum','N':'sum','L':'sum'})
    mrallt.columns=['Allenatore','Media Punti 3W','Squadre','Panchine','V','N','P']
    mrallt['Squadre'] = [sorted(set(x)) for x in mrallt['Squadre']]
    mrallt['Squadre'] = mrallt['Squadre'].apply(lambda x: ', '.join(map(str, x)))
    mrallt = mrallt.sort_values(by=['Panchine'], ascending=False)
    return mrallt

def match_series(dati,team,c_t):
    db=dati[(dati[c_t] == team)].sort_values('Data')
    db['Risultato']=[str(x)+'-'+str(y) for x,y in zip(db['GC'],db['GT'])]
    if c_t=='CASA':
        db=db.rename(columns={'GC':'Gol Fatti','GT':'Gol subiti'})
    else:
        db = db.rename(columns={'GT': 'Gol Fatti', 'GC': 'Gol subiti'})
    db['Esito']=['W' if x>y else 'N' if x==y else 'L' for x,y in zip(db['Gol Fatti'],db['Gol subiti'])]
    sin_count = noloss_count = nowin_count = gf_count = gs_count = 0
    prev_esit = None
    list_single, list_noloss, list_nowin, list_gf, list_gs = [],[],[],[],[]
    for e,gf,gs in zip(db['Esito'],db['Gol Fatti'],db['Gol subiti']):
        sin_count = sin_count + 1 if e == prev_esit else 1
        noloss_count = noloss_count + 1 if e != 'L' else 0
        nowin_count = nowin_count + 1 if e != 'W' else 0
        gf_count = gf_count + 1 if gf != 0 else 0
        gs_count = gs_count + 1 if gs == 0 else 0
        list_single.append(sin_count)
        list_noloss.append(noloss_count)
        list_nowin.append(nowin_count)
        list_gf.append(gf_count)
        list_gs.append(gs_count)
        prev_esit = e
    db['Single']=list_single
    db['No loss']=list_noloss
    db['No win']=list_nowin
    db['Gf consec']=list_gf
    db['Clean sheet']=list_gs
    return db

def match_series_tot(dati,team):
    home_ser=match_series(dati,team,c_t='CASA')
    away_ser=match_series(dati,team,c_t='TRAS')
    home_ser1=home_ser.drop(['Single','No loss','No win','Gf consec','Clean sheet'],axis=1)
    away_ser1 = away_ser.drop(['Single', 'No loss', 'No win', 'Gf consec', 'Clean sheet'], axis=1)
    db=pd.concat([home_ser1,away_ser1],ignore_index=True).sort_values('Data')
    sin_count = noloss_count = nowin_count = gf_count = gs_count = 0
    prev_esit = None
    list_single, list_noloss, list_nowin, list_gf, list_gs = [],[],[],[],[]
    for e,gf,gs in zip(db['Esito'],db['Gol Fatti'],db['Gol subiti']):
        sin_count = sin_count + 1 if e == prev_esit else 1
        noloss_count = noloss_count + 1 if e != 'L' else 0
        nowin_count = nowin_count + 1 if e != 'W' else 0
        gf_count = gf_count + 1 if gf != 0 else 0
        gs_count = gs_count + 1 if gs == 0 else 0
        list_single.append(sin_count)
        list_noloss.append(noloss_count)
        list_nowin.append(nowin_count)
        list_gf.append(gf_count)
        list_gs.append(gs_count)
        prev_esit = e
    db['Single']=list_single
    db['No loss']=list_noloss
    db['No win']=list_nowin
    db['Gf consec']=list_gf
    db['Clean sheet']=list_gs
    return [db, home_ser, away_ser]

def match_series_mod(dati,team,choice):
    col_fin=['Stagione','Giorno','CASA','TRAS','Risultato']
    if choice=='Tot':
        db_ser_tot = match_series_tot(dati,team=team)[0]
    elif choice=='C':
        db_ser_tot = match_series_tot(dati,team=team)[1]
    else:
        db_ser_tot = match_series_tot(dati,team=team)[2]
    db_ser_tot['nrow'] = list(range(1, db_ser_tot.shape[0] + 1))
    db_ser_tot_w = db_ser_tot[db_ser_tot['Esito'] == 'W']
    db_ser_tot_w = db_ser_tot_w.sort_values(['Single', 'Data'], ascending=False)
    db_ser_tot_w.reset_index(drop=True, inplace=True)
    record_wc = db_ser_tot_w.loc[0, 'Single'].item()
    record_wc_nr = db_ser_tot_w.loc[0, 'nrow'].item()
    df_serie_wc = db_ser_tot.iloc[record_wc_nr - record_wc:record_wc_nr, :]

    db_ser_tot_nl = db_ser_tot.sort_values(['No loss', 'Data'], ascending=False)
    db_ser_tot_nl.reset_index(drop=True, inplace=True)
    record_nl = db_ser_tot_nl.loc[0, 'No loss'].item()
    record_nl_nr = db_ser_tot_nl.loc[0, 'nrow'].item()
    df_serie_nl = db_ser_tot.iloc[record_nl_nr - record_nl:record_nl_nr, :]

    db_ser_tot_gfc = db_ser_tot.sort_values(['Gf consec', 'Data'], ascending=False)
    db_ser_tot_gfc.reset_index(drop=True, inplace=True)
    record_gfc = db_ser_tot_gfc.loc[0, 'Gf consec'].item()
    record_gfc_nr = db_ser_tot_gfc.loc[0, 'nrow'].item()
    df_serie_gfc = db_ser_tot.iloc[record_gfc_nr - record_gfc:record_gfc_nr, :]

    db_ser_tot_l = db_ser_tot[db_ser_tot['Esito'] == 'L']
    db_ser_tot_l = db_ser_tot_l.sort_values(['Single', 'Data'], ascending=False)
    db_ser_tot_l.reset_index(drop=True, inplace=True)
    record_lc = db_ser_tot_l.loc[0, 'Single'].item()
    record_lc_nr = db_ser_tot_l.loc[0, 'nrow'].item()
    df_serie_lc = db_ser_tot.iloc[record_lc_nr - record_lc:record_lc_nr, :]

    db_ser_tot_nw = db_ser_tot.sort_values(['No win', 'Data'], ascending=False)
    db_ser_tot_nw.reset_index(drop=True, inplace=True)
    record_nw = db_ser_tot_nw.loc[0, 'No win'].item()
    record_nw_nr = db_ser_tot_nw.loc[0, 'nrow'].item()
    df_serie_nw = db_ser_tot.iloc[record_nw_nr - record_nw:record_nw_nr, :]

    db_ser_tot_gsc = db_ser_tot.sort_values(['Clean sheet', 'Data'], ascending=False)
    db_ser_tot_gsc.reset_index(drop=True, inplace=True)
    record_gsc = db_ser_tot_gsc.loc[0, 'Clean sheet'].item()
    record_gsc_nr = db_ser_tot_gsc.loc[0, 'nrow'].item()
    df_serie_gsc = db_ser_tot.iloc[record_gsc_nr - record_gsc:record_gsc_nr, :]
    return [df_serie_wc[col_fin], record_wc,
            df_serie_nl[col_fin], record_nl,
            df_serie_gfc[col_fin], record_gfc,
            df_serie_lc[col_fin], record_lc,
            df_serie_nw[col_fin], record_nw,
            df_serie_gsc[col_fin], record_gsc]

def prec(dati,t1,t2):
    t1h=dati[(dati['CASA']==t1) & (dati['TRAS']==t2)]
    t2h = dati[(dati['CASA'] == t2) & (dati['TRAS'] == t1)]
    t1h['WH']=[1 if x>y else 0 for x,y in zip(t1h['GC'],t1h['GT'])]
    t1h['N'] = [1 if x == y else 0 for x, y in zip(t1h['GC'], t1h['GT'])]
    t1h['WA'] = [1 if x < y else 0 for x, y in zip(t1h['GC'], t1h['GT'])]
    t1h['Prec cum']=[1 if x==1 else -1 if y==1 else 0 for x,y in zip(t1h['WH'],t1h['WA'])]
    t2h['WH'] = [1 if x > y else 0 for x, y in zip(t2h['GC'], t2h['GT'])]
    t2h['N'] = [1 if x == y else 0 for x, y in zip(t2h['GC'], t2h['GT'])]
    t2h['WA'] = [1 if x < y else 0 for x, y in zip(t2h['GC'], t2h['GT'])]
    t2h['Prec cum'] = [1 if x == 1 else -1 if y == 1 else 0 for x, y in zip(t2h['WA'], t2h['WH'])]
    t1h_gr = t1h.groupby('CASA',as_index=False).agg({'TRAS':'count','WH':'sum','N':'sum','WA':'sum','GC':'sum','GT':'sum'})
    t1h_gr['Bil']=[x-y for x,y in zip(t1h_gr['WH'],t1h_gr['WA'])]
    t2h_gr = t2h.groupby('CASA',as_index=False).agg({'TRAS':'count','WH':'sum','N':'sum','WA':'sum','GC':'sum','GT':'sum'})
    t2h_gr['Bil'] = [x - y for x, y in zip(t2h_gr['WH'], t2h_gr['WA'])]
    cum_prec = pd.concat([t1h[['Stagione','Prec cum']],t2h[['Stagione','Prec cum']]])
    cum_prec = cum_prec.groupby('Stagione',as_index=False).agg({'Prec cum':'sum'})
    cum_prec['CumPr'] = cum_prec['Prec cum'].cumsum()
    return [t1h_gr, t2h_gr, cum_prec]

def prec_with_mr(dati,type,i1,i2):
    if type=='MM':
        t1h = dati[(dati['All CASA'] == i1) & (dati['All TRAS'] == i2)]
        t2h = dati[(dati['All CASA'] == i2) & (dati['All TRAS'] == i1)]
    else:
        t1h = dati[(dati['All CASA'] == i1) & (dati['TRAS'] == i2)]
        t2h = dati[(dati['CASA'] == i2) & (dati['All TRAS'] == i1)]
    t1h['W1']=[1 if x>y else 0 for x,y in zip(t1h['GC'],t1h['GT'])]
    t1h['N']=[1 if x == y else 0 for x, y in zip(t1h['GC'], t1h['GT'])]
    t1h['W2'] = [1 if x < y else 0 for x, y in zip(t1h['GC'], t1h['GT'])]
    t2h['W1'] = [1 if x < y else 0 for x, y in zip(t2h['GC'], t2h['GT'])]
    t2h['N'] = [1 if x == y else 0 for x, y in zip(t2h['GC'], t2h['GT'])]
    t2h['W2'] = [1 if x > y else 0 for x, y in zip(t2h['GC'], t2h['GT'])]
    tot_gio = t1h.shape[0]+t2h.shape[0]
    return [tot_gio, sum(t1h['W1'])+sum(t2h['W1']), sum(t1h['N'])+sum(t2h['N']), sum(t1h['W2'])+sum(t2h['W2'])]

def riepilogo_prec(dati,type,i1):
    if type=='TT':
        df_tt1 = dati[(dati['CASA'] == i1) | (dati['TRAS'] == i1)]
        df_tt1['Opponent'] = [x if x != i1 else y for x, y in zip(df_tt1['CASA'], df_tt1['TRAS'])]
        df_tt1['W'] = [1 if ((x == i1) & (y > z) | (x != i1) & (z > y)) else 0 for x, y, z in
                       zip(df_tt1['CASA'], df_tt1['GC'], df_tt1['GT'])]
        df_tt1['D'] = [1 if x == y else 0 for x, y in zip(df_tt1['GC'], df_tt1['GT'])]
        df_tt1['L'] = [1 if ((x == i1) & (y < z) | (x != i1) & (z < y)) else 0 for x, y, z in
                       zip(df_tt1['CASA'], df_tt1['GC'], df_tt1['GT'])]
        df_tt1_g = df_tt1.groupby('Opponent', as_index=False).agg(
            {'CASA': 'count', 'W': 'sum', 'D': 'sum', 'L': 'sum'}).sort_values(['CASA', 'W'])
        df_tt1_g['Bil'] = [x - y for x, y in zip(df_tt1_g['W'], df_tt1_g['L'])]
    elif type=='MM':
        df_tt1 = dati[(dati['All CASA'] == i1) | (dati['All TRAS'] == i1)]
        df_tt1['Opponent'] = [x if x != i1 else y for x, y in zip(df_tt1['All CASA'], df_tt1['All TRAS'])]
        df_tt1['W'] = [1 if ((x == i1) & (y > z) | (x != i1) & (z > y)) else 0 for x, y, z in
                       zip(df_tt1['All CASA'], df_tt1['GC'], df_tt1['GT'])]
        df_tt1['D'] = [1 if x == y else 0 for x, y in zip(df_tt1['GC'], df_tt1['GT'])]
        df_tt1['L'] = [1 if ((x == i1) & (y < z) | (x != i1) & (z < y)) else 0 for x, y, z in
                       zip(df_tt1['All CASA'], df_tt1['GC'], df_tt1['GT'])]
        df_tt1_g = df_tt1.groupby('Opponent', as_index=False).agg(
            {'All CASA': 'count', 'W': 'sum', 'D': 'sum', 'L': 'sum'}).sort_values(['All CASA', 'W'])
        df_tt1_g['Bil'] = [x - y for x, y in zip(df_tt1_g['W'], df_tt1_g['L'])]
    else:
        df_tt1 = dati[(dati['All CASA'] == i1) | (dati['All TRAS'] == i1)]
        df_tt1['Opponent'] = [z if x != i1 else w for x, z, w in zip(df_tt1['All CASA'], df_tt1['CASA'], df_tt1['TRAS'])]
        df_tt1['W'] = [1 if ((x == i1) & (y > z) | (x != i1) & (z > y)) else 0 for x, y, z in
                       zip(df_tt1['All CASA'], df_tt1['GC'], df_tt1['GT'])]
        df_tt1['D'] = [1 if x == y else 0 for x, y in zip(df_tt1['GC'], df_tt1['GT'])]
        df_tt1['L'] = [1 if ((x == i1) & (y < z) | (x != i1) & (z < y)) else 0 for x, y, z in
                       zip(df_tt1['All CASA'], df_tt1['GC'], df_tt1['GT'])]
        df_tt1_g = df_tt1.groupby('Opponent', as_index=False).agg(
            {'All CASA': 'count', 'W': 'sum', 'D': 'sum', 'L': 'sum'}).sort_values(['All CASA', 'W'])
        df_tt1_g['Bil'] = [x - y for x, y in zip(df_tt1_g['W'], df_tt1_g['L'])]
    df_tt1_g.reset_index(drop=True, inplace=True)
    return df_tt1_g

def ris_parz(datis,datim):
    mar_arr=datim.merge(datis[['ID','CASA','TRAS']],on='ID',how='left')
    mar_arr['delta_gc']=[1 if x==y else 0 for x,y in zip(mar_arr['Squadra'],mar_arr['CASA'])]
    mar_arr['delta_gt']=[1 if x==y else 0 for x,y in zip(mar_arr['Squadra'],mar_arr['TRAS'])]
    mar_arr=mar_arr.sort_values(['ID','Minuto','Recupero'],ascending=True)
    mar_arr['GC_parz'] = mar_arr.groupby('ID')['delta_gc'].cumsum()
    mar_arr['GT_parz'] = mar_arr.groupby('ID')['delta_gt'].cumsum()

    mar_1t = mar_arr[mar_arr['Minuto'] <= 45]
    mar_1t['min_tot'] = [x + y if not pd.isna(y) else x for x, y in zip(mar_1t['Minuto'], mar_1t['Recupero'])]
    mar_1t_max = mar_1t.groupby(['ID'], as_index=False).agg({'min_tot': 'max'})
    mar_1t_max = mar_1t_max.merge(mar_1t, on=['ID', 'min_tot'], how='inner')
    df_fin = datis.merge(mar_1t_max[['ID', 'GC_parz', 'GT_parz']], on='ID', how='left')
    df_fin['GC_parz']=df_fin['GC_parz'].fillna(0)
    df_fin['GT_parz']=df_fin['GT_parz'].fillna(0)
    df_fin['GC_parz']=[int(x) for x in df_fin['GC_parz']]
    df_fin['GT_parz'] = [int(x) for x in df_fin['GT_parz']]
    return [df_fin, mar_arr]

def class_1t(datis,datim,seas):
    db = ris_parz(datis,datim)[0]
    db = db[(db['Stagione'] == seas)]
    db['H']=[1 if x>y else 0 for x,y in zip(db['GC_parz'],db['GT_parz'])]
    db['N']=[1 if x==y else 0 for x,y in zip(db['GC_parz'],db['GT_parz'])]
    db['A']=[1 if x<y else 0 for x,y in zip(db['GC_parz'],db['GT_parz'])]
    db['PH']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['H'],db['N'],db['Stagione'])]
    db['PA']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['A'],db['N'],db['Stagione'])]
    casa=db.groupby(['CASA'],as_index=False).agg({'PH':'sum','Data':'count','H':'sum','N':'sum','A':'sum','GC_parz':'sum','GT_parz':'sum'})
    trasferta=db.groupby(['TRAS'],as_index=False).agg({'PA':'sum','Data':'count','A':'sum','N':'sum','H':'sum','GT_parz':'sum','GC_parz':'sum'})
    casa.columns=['Squadra','Punti','Gio','V','N','P','GF','GS']
    trasferta.columns=['Squadra','Punti','Gio','V','N','P','GF','GS']
    classifica=pd.concat([casa,trasferta],ignore_index=True).groupby(['Squadra'],as_index=False).agg({'Punti':'sum','Gio':'sum','V':'sum','N':'sum','P':'sum','GF':'sum','GS':'sum'})
    classifica=classifica.sort_values('Punti',ascending=False)
    return classifica

def change_1t_2t(datis,datim,seas):
    db=ris_parz(datis,datim)[0]
    db = db[(db['Stagione'] == seas)]
    db['1t/2t H']=['V/V' if (x>y) & (x1>y1) else 'N/V' if (x>y) & (x1==y1) else 'P/V' if (x>y) & (x1<y1)
                   else 'V/N' if (x==y) & (x1>y1) else 'V/P' if (x<y) & (x1>y1) else 'N/P' if (x<y) & (x1==y1) else
                   'P/N' if (x==y) & (x1<y1) else 'P/P' if (x<y) & (x1<y1) else 'N/N' for x,y,x1,y1 in zip(db['GC'],db['GT'],db['GC_parz'],db['GT_parz'])]
    db['1t/2t A']=['V/V' if x=='P/P' else 'N/P' if x=='N/V' else 'V/P' if x=='P/V' else 'P/N' if x=='V/N'
                    else 'P/V' if x=='V/P' else 'N/V' if x=='N/P' else 'V/N' if x=='P/N' else 'V/V' if x=='P/P' else 'N/N' for x in db['1t/2t H']]
    db_casa=db[['CASA','1t/2t H']]
    db_tras = db[['TRAS', '1t/2t A']]
    db_casa.columns=['Squadre','1t/2t']
    db_tras.columns = ['Squadre', '1t/2t']
    db_fin=pd.concat([db_casa,db_tras])
    df_pivot = db_fin.pivot_table(index='Squadre', columns='1t/2t',aggfunc='size')
    df_pivot = df_pivot[['V/V','V/N','V/P','N/V','N/N','N/P','P/V','P/N','P/P']]
    df_pivot = df_pivot.fillna(0)
    return df_pivot

def min_advantage(datis,datim,seas):
    db = ris_parz(datis, datim)[1]
    seas_select=[x for x in db['ID'] if x[:6]==seas.split('-')[0]+seas.split('-')[1]]
    db = db[db['ID'].isin(seas_select)]
    db['team_adv'] = [w if y > z else x if z > y else 'Pari' for w, x, y, z in
                           zip(db['CASA'], db['TRAS'], db['GC_parz'], db['GT_parz'])]
    min_diff_goal = []
    db.reset_index(drop=True, inplace=True)
    for r in list(range(db.shape[0] - 1)):
        if db.loc[r, 'ID'] == db.loc[r + 1, 'ID']:
            min_diff_goal.append(max(int(db.loc[r + 1, 'Minuto']) - int(db.loc[r, 'Minuto']), 1))
        else:
            min_diff_goal.append(max(90 - int(db.loc[r, 'Minuto']), 1))
    min_diff_goal.append(max(90 - int(db.loc[r + 1, 'Minuto']), 1))
    db['min_adv'] = min_diff_goal
    db_adv = db.groupby(['ID', 'CASA', 'TRAS', 'team_adv'], as_index=False).agg({'min_adv': 'sum'})
    h_adv = db_adv[db_adv['CASA'] == db_adv['team_adv']]
    h_adv['team_sv'] = h_adv['TRAS']
    a_adv = db_adv[db_adv['TRAS'] == db_adv['team_adv']]
    a_adv['team_sv'] = a_adv['CASA']
    db_fin = pd.concat([h_adv, a_adv])
    db_fin_v = db_fin.groupby('team_adv', as_index=False).agg({'min_adv': 'sum'})
    db_fin_v.columns = ['Squadre', 'Vantaggio']
    db_fin_sv = db_fin.groupby('team_sv', as_index=False).agg({'min_adv': 'sum'})
    db_fin_sv.columns = ['Squadre', 'Svantaggio']
    van_svan = db_fin_v.merge(db_fin_sv, on='Squadre', how='left')

    # parte pareggi
    paregg = db_adv[db_adv['team_adv'] == 'Pari']
    pg1 = paregg.groupby('CASA', as_index=False).agg({'min_adv': 'sum'})
    pg1 = pg1.rename(columns={'min_adv': 'Minuto'})
    pg2 = paregg.groupby('TRAS', as_index=False).agg({'min_adv': 'sum'})
    pg2 = pg2.rename(columns={'min_adv': 'Minuto'})
    pgmin = db.groupby(['CASA', 'TRAS'], as_index=False).agg({'Minuto': 'min'})
    pgmin1 = pgmin.groupby('CASA', as_index=False).agg({'Minuto': 'sum'})
    pgmin2 = pgmin.groupby('TRAS', as_index=False).agg({'Minuto': 'sum'})
    pg1fin = pd.concat([pg1, pgmin1])
    pg2fin = pd.concat([pg2, pgmin2])
    pg1fin = pg1fin.rename(columns={'CASA': 'Squadre'})
    pg2fin = pg2fin.rename(columns={'TRAS': 'Squadre'})
    pgfin = pd.concat([pg1fin, pg2fin])
    pgfin = pgfin.groupby('Squadre', as_index=False).agg({'Minuto': 'sum'})

    zer_zer = datis[(datis['GC'] == 0) & (datis['GT'] == 0) & (datis['Stagione']==seas)]
    zer_zerh = zer_zer.groupby('CASA', as_index=False).agg({'Giornata': 'count'})
    zer_zera = zer_zer.groupby('TRAS', as_index=False).agg({'Giornata': 'count'})
    zer_zerh = zer_zerh.rename(columns={'CASA': 'Squadre'})
    zer_zera = zer_zera.rename(columns={'TRAS': 'Squadre'})
    zer_zer_fin = pd.concat([zer_zerh, zer_zera]).groupby('Squadre', as_index=False).agg({'Giornata': 'sum'})
    zer_zer_fin['min_par'] = [x * 90 for x in zer_zer_fin['Giornata']]
    pg_complet = pgfin.merge(zer_zer_fin, on='Squadre', how='left')
    pg_complet['Pareggio'] = [x + int(y) if not np.isnan(y) else x for x, y in
                              zip(pg_complet['Minuto'], pg_complet['min_par'])]

    van_svan_par = van_svan.merge(pg_complet[['Squadre', 'Pareggio']], on='Squadre', how='left')
    van_svan_par['Tot'] = [x + y + z for x, y, z in
                           zip(van_svan_par['Vantaggio'], van_svan_par['Svantaggio'], van_svan_par['Pareggio'])]
    van_svan_par['Vantaggio'] = [round((x / y) * 90,2) for x, y in zip(van_svan_par['Vantaggio'], van_svan_par['Tot'])]
    van_svan_par['Svantaggio'] = [round((x / y) * 90,2) for x, y in zip(van_svan_par['Svantaggio'], van_svan_par['Tot'])]
    van_svan_par['Pareggio'] = [round((x / y) * 90,2) for x, y in zip(van_svan_par['Pareggio'], van_svan_par['Tot'])]
    return van_svan_par

def color_coding(row,c1,c2,t1):
    score_home, score_away = map(int, risultato.split('-'))
    if ((score_home>score_away) & (row['CASA']==t1)) | ((score_home<score_away) & (row['TRAS']==t1)):
        bg=[f'background-color:{c1}'] * len(row)
    elif ((score_home<score_away) & (row['CASA']==t1)) | ((score_home>score_away) & (row['TRAS']==t1)):
        bg=[f'background-color:{c2}'] * len(row)
    else:
        bg=['background-color:black']* len(row)
    return bg