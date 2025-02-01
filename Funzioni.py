import pandas as pd
import numpy as np
from datetime import date
import streamlit as st
from github import Github

conn_g=Github(st.secrets['TOKEN'])
repo_seriea=conn_g.get_user("tommyblasco").get_repo("SerieA_History")

@st.cache
def load_data(df):
    if df!='Penalizzazioni':
        l_data = pd.read_csv("https://raw.githubusercontent.com/tommyblasco/SerieA_History/refs/heads/main/Dati/" + df + ".csv",
                             sep=",", decimal=".", parse_dates=['Data'], dayfirst=True)
    else:
        l_data = pd.read_csv("https://raw.githubusercontent.com/tommyblasco/SerieA_History/refs/heads/main/Dati/" + df + ".csv",
                             sep=",", decimal=".", parse_dates=['Da','A'], dayfirst=True)
    return l_data

storico=load_data("Partite")
tbd=load_data("TBD")
penalita=load_data("Penalizzazioni")

#classifica x tutte le stagioni
def ranking(seas,st_date=date(1900,1,1),en_date=date.today()):
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
        else:
            new_class=classifica
    else:
        new_class=classifica[['Squadra','Gio','V','N','P','GF','GS']]
    return new_class