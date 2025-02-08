import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import streamlit as st
from github import Github
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

conn_g=Github(st.secrets['TOKEN'])
repo_seriea=conn_g.get_user("tommyblasco").get_repo("SerieA_History")

def load_data(df):
    if df!='Penalizzazioni':
        l_data = pd.read_csv(f"https://raw.githubusercontent.com/tommyblasco/SerieA_History/refs/heads/main/Dati/{df}.csv",
                             sep=",", decimal=".", parse_dates=['Data'], dayfirst=True)
    else:
        l_data = pd.read_csv(f"https://raw.githubusercontent.com/tommyblasco/SerieA_History/refs/heads/main/Dati/{df}.csv",
                             sep=",", decimal=".", parse_dates=['Da','A'], dayfirst=True)
    return l_data

def load_images(team,yyyy):
    stemmi_ava=repo_seriea.get_dir_contents(f"images/stemmi/{team}/".replace(' ','%20'))
    file_names = [file.name.split(".")[0] for file in stemmi_ava]
    yy_sel=min([x for x in file_names if x>=yyyy])
    url_stemma=f"https://raw.githubusercontent.com/tommyblasco/SerieA_History/tree/main/images/stemmi/{team}/{yy_sel}.png".replace(' ','%20')
    return url_stemma

storico=load_data("Partite")
tbd=load_data("TBD")
penalita=load_data("Penalizzazioni")

#classifica x tutte le stagioni
def ranking(seas,st_date=datetime(1900,1,1),en_date=datetime.now()):
    if seas=='All':
        db=storico
    else:
        db=storico[(storico['Stagione']==seas) & (storico['Data']>=st_date) & (storico['Data']<=en_date)]
    db['H']=[1 if x>y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['N']=[1 if x==y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['A']=[1 if x<y else 0 for x,y in zip(db['GC'],db['GT'])]
    db['PH']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['H'],db['N'],db['Stagione'])]
    db['PA']=[x*3+y if z>='1994-95' else x*2+y for x,y,z in zip(db['A'],db['N'],db['Stagione'])]
    casa=db.groupby(['CASA'],as_index=False).agg({'PH':'sum','Data':'count','H':'sum','N':'sum','A':'sum','GC':'sum','GT':'sum'})
    trasferta=db.groupby(['TRAS'],as_index=False).agg({'PA':'sum','Data':'count','A':'sum','N':'sum','H':'sum','GT':'sum','GC':'sum'})
    casa['DRC']=[x-y for x,y in zip(casa['GC'],casa['GT'])]
    trasferta['DRT']=[x-y for x,y in zip(casa['GT'],casa['GC'])]
    casa.columns=['Squadra','Punti','Gio','V','N','P','GF','GS','DR']
    trasferta.columns=['Squadra','Punti','Gio','V','N','P','GF','GS','DR']
    classifica=pd.concat([casa,trasferta],ignore_index=True).groupby(['Squadra'],as_index=False).agg({'Punti':'sum','Gio':'sum','V':'sum','N':'sum','P':'sum','GF':'sum','GS':'sum','DR':'sum'})
    if seas!='All':
        pen_fil=penalita[(penalita['Stagione']==seas) & (penalita['A']>=en_date)]
        if pen_fil.shape[0]>0:
            new_class = classifica.merge(pen_fil[['Squadra','Pen']], on='Squadra',how='left')
            new_class['Pnt']=new_class['Punti']-new_class['Pen']
            new_class=new_class[['Squadra','Pnt','Gio','V','N','P','GF','GS','DR']]
            new_class = new_class.sort_values(by=['Pnt', 'DR'], ascending=False)
        else:
            new_class=classifica.sort_values(by=['Punti', 'DR'], ascending=False)
    else:
        new_class=classifica[['Squadra','Gio','V','N','P','GF','GS']]
        new_class = new_class.sort_values(by=['Gio'], ascending=False)
    new_class.insert(0,'Rk',range(1,new_class.shape[0]+1))
    return new_class

#gen vincitori
def albo(sl):
    vin, stem = [],[]
    for s in sl:
        cl_se=ranking(seas=s)
        team_win=cl_se.iloc[0,1]
        stem.append(load_images(team_win,s[:4]))
        vin.append(team_win)
    return {k:[v1,v2] for k,v1,v2 in zip(sl,vin,stem)}

#prossima giornata avendo anche il rif alla posizione della squadra
def nx_match_rank(s,n):
    team_list = ranking(seas=s)[['Rk','Squadra']]
    prox_partite = tbd[tbd['Data']<datetime.now()+timedelta(days=n)][['Giornata','Data','CASA','TRAS']]

    rank_h = prox_partite.merge(team_list, left_on='CASA', right_on='Squadra', how='left').drop('Squadra', axis=1)
    rank_h.rename(columns={'rank': 'rank_h'},inplace=True)
    rank_a = rank_h.merge(team_list, left_on='TRAS', right_on='Squadra', how='left').drop('Squadra', axis=1)
    rank_a.rename(columns={'rank': 'rank_a'},inplace=True)
    rank_a['Home'] = [x + ' (' + str(y) + '.)' for x, y in zip(rank_a['CASA'], rank_a['rank_h'])]
    rank_a['Away'] = [x + ' (' + str(y) + '.)' for x, y in zip(rank_a['TRAS'], rank_a['rank_a'])]
    rank_a = rank_a[['Giornata', 'Data', 'Home', 'Away']]
    rank_a['Data']=rank_a['Data'].dt.date
    return rank_a