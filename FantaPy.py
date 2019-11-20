# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 21:17:50 2019

@author: user
"""
import numpy as np
from datetime import date
import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import dateparser
import flask
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table_experiments as dt
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import dash_table


#from __future__ import print_function
#import pickle
#import os.path
#from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
#
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#
#SAMPLE_SPREADSHEET_ID = ['1y6pzeMbKg3ssqlxKLTMdqfIARL-x6THsGF_Hu56Ndvw', #gioc
#'10gDSnddSuaHa1Do28Pin-TmzcJ8hpOdLDU52QMDPQZg', #quotazioni
#'1JaEZbjCaob8IYioTcNXoFO0v6WuBePrKseXILmSLxHI', #mercato
#'1TNY-Ps8bdkPyo-wZS9rkzHvbRnCru10vD9LjeaCd83A', #part cup
#'1Z5s-3KncSmt0IsbWgjNo2VWtG5x97BTzkIvIwl70tTM', #part fanta
#'1PV9aSp9LVJtyPTNrbNkRRfGgXYiCavXx-cZRZqJKlCg', #voti
#'1LxD8lUYmH4m6lAd7FVdzVbEUTu1HfIVkmpoAu3DJUE0'] #ruolo
#SAMPLE_RANGE_NAME = 'Foglio1'
#
#def google():
#    """Shows basic usage of the Sheets API.
#    Prints values from a sample spreadsheet.
#    """
#    creds = None
#    # The file token.pickle stores the user's access and refresh tokens, and is
#    # created automatically when the authorization flow completes for the first
#    # time.
#    if os.path.exists('token.pickle'):
#        with open('token.pickle', 'rb') as token:
#            creds = pickle.load(token)
#    # If there are no (valid) credentials available, let the user log in.
#    if not creds or not creds.valid:
#        if creds and creds.expired and creds.refresh_token:
#            creds.refresh(Request())
#        else:
#            flow = InstalledAppFlow.from_client_secrets_file(
#                'credentials.json', SCOPES)
#            creds = flow.run_local_server(port=0)
#        # Save the credentials for the next run
#        with open('token.pickle', 'wb') as token:
#            pickle.dump(creds, token)
#
#    service = build('sheets', 'v4', credentials=creds)
#
#    # Call the Sheets API
#    sheet = service.spreadsheets()
#    df=[]
#    for i in SAMPLE_SPREADSHEET_ID:
#        result = sheet.values().get(spreadsheetId=i,
#                                    range=SAMPLE_RANGE_NAME).execute()
#        values = result.get('values', [])
#        df.append(pd.DataFrame(values[1:],columns=values[0]) )   
#    return df
import os

giocatori=pd.read_csv(os.path.join('/Users/user/Desktop/Fantacalcio/Flask app','Gioc.csv'),sep=";").drop(['Unnamed: 6','Unnamed: 7'],axis=1)
ruolo=pd.read_csv(os.path.join('/Users/user/Desktop/Fantacalcio/Flask app','Ruolo.csv'),sep=";")
coppa=pd.read_csv(os.path.join('/Users/user/Desktop/Fantacalcio/Flask app','Partite cup.csv'),sep=";").iloc[:41,:]
voti=pd.read_csv(os.path.join('/Users/user/Desktop/Fantacalcio/Flask app','Voti.csv'),sep=";")
quotazioni=pd.read_csv(os.path.join('/Users/user/Desktop/Fantacalcio/Flask app','Quotazioni.csv'),sep=";")
mercato=pd.read_csv(os.path.join('/Users/user/Desktop/Fantacalcio/Flask app','Mercato.csv'),sep=";")
partite=pd.read_csv(os.path.join('/Users/user/Desktop/Fantacalcio/Flask app','Partite fanta.csv'),sep=";")
partite['Pnt casa']=[float(str(x).replace(',','.')) for x in partite['Pnt casa']]
partite['Pnt tras']=[float(str(x).replace(',','.')) for x in partite['Pnt tras']]
coppa['Pnt casa']=[float(str(x).replace(',','.')) for x in coppa['Pnt casa']]
coppa['Pnt tras']=[float(str(x).replace(',','.')) for x in coppa['Pnt tras']]    
mercato['Spesa A']=[float(str(x).replace(',','.')) for x in mercato['Spesa A']]
mercato['Entrata Da']=[float(str(x).replace(',','.')) for x in mercato['Entrata Da']] 
mercato['Costo contratto']=[float(str(x).replace(',','.')) for x in mercato['Costo contratto']] 
quotazioni['VI']=[float(str(x).replace(',','.')) for x in quotazioni['VI']] 
quotazioni['VA']=[float(str(x).replace(',','.')) for x in quotazioni['VA']] 
voti['Voto']=[float(str(x).replace(',','.')) for x in voti['Voto']] 
giocatori['Data_nascita']=pd.to_datetime(giocatori['Data_nascita'],format='%Y-%m-%d')
mercato['Data']=pd.to_datetime(mercato['Data'],format='%d/%m/%Y')
mercato['TP']=pd.to_datetime(mercato['TP'],format='%d/%m/%Y')
voti['Data']=pd.to_datetime(voti['Data'],format='%Y-%m-%d')

#print(ruolo)
#print(voti)
voti_arr=pd.merge(voti,ruolo[['Nome','Ruolo']],on='Nome',how='left')
voti_arr=voti_arr.assign(PI=0)
voti_arr.loc[(voti_arr['Gs']==0) & (voti_arr['Ruolo']=='Por'),'PI']=1
voti_arr['Stipendio']=voti_arr['Gf']*0.15+voti_arr['Rp']*0.15+voti_arr['Rf']*0.1+voti_arr['Ass']*0.05+voti_arr['PI']*0.05

sqlquery=''' 
select * , b.A 
from voti_arr as a 
left join  (select A, Nome, Data, TP from mercato) as b on 
a.Nome=b.Nome and a.Data between b.Data and b.TP
'''
tab_voti=ps.sqldf(sqlquery,locals())
tab_voti=tab_voti.iloc[:,1:19]
FV=[tab_voti.iloc[x,2]+tab_voti.iloc[x,3]*3-tab_voti.iloc[x,4]+tab_voti.iloc[x,5]*3-tab_voti.iloc[x,6]+tab_voti.iloc[x,7]*2-tab_voti.iloc[x,8]*2-tab_voti.iloc[x,9]*.5-tab_voti.iloc[x,10]+tab_voti.iloc[x,11] for x in range(tab_voti.shape[0])]
tab_voti=pd.concat([tab_voti,pd.DataFrame({'FV':FV})],axis=1)

# ***** ANAGRAFICA GIOCATORI SQUADRE *****
m_filt=mercato[(date.today()>=mercato['Data']) & (date.today()<mercato['TP'])]
ana1=pd.merge(giocatori,m_filt[['A','Tipo_operazione','TP','Nome']], left_on='ID',right_on='Nome',how='inner')
ana1=ana1.iloc[:,0:9]
ana2=pd.merge(ana1,ruolo[['Ruolo','Nome']], left_on='ID',right_on='Nome',how='inner')
ana2=ana2.iloc[:,0:10]
ana_gio=pd.merge(ana2,quotazioni[['VA','Nome','Diff']], left_on='ID',right_on='Nome',how='inner')
ana_gio=ana_gio.iloc[:,0:11]
ana_gio.columns=['Nome','Nome completo','Data nascita','Luogo nascita','Nazionalità','Età','Squadra','Tipo contratto','Fine prestazione','Ruolo','Valore']
ana_gio['Valore']=round(ana_gio['Valore'],2)
ana_gio.to_excel(r'C:\Users\user\Desktop\Fanta dati db\per tablo\anag.xlsx',index=None,header=True)

#****** BILANCIO *******
entrate_tr=[]
entrate_in=[]
uscite_tr=[]
uscite_pr=[]
uscite_rn=[]
uscite_sv=[]
contracts=[]
stip=[]
squad=[]
quota_p=[]
premi=[0]*10
fl_st=mercato[(mercato['Data']>date(2019,7,1)) & (mercato['Data']<date(2020,7,1))]
t_list=list(fl_st.A.unique())
for t in t_list:
    df_filt_tr=fl_st[(fl_st['Da']==t) & (fl_st['Tipo_operazione'].str.match('D')|fl_st['Tipo_operazione'].str.match('P'))]
    entrate_tr.append(round(sum(df_filt_tr['Entrata Da']),2))
    #INDENNIZZI
    df_filt_in=fl_st[(fl_st['Da']==t) & (fl_st['Tipo_operazione'].str.match('I'))]
    entrate_in.append(round(sum(df_filt_tr['Entrata Da']),2))
    #DEFINITIVI
    df_filt1_tr=fl_st[(fl_st['A']==t) & (fl_st['Tipo_operazione'].str.match('D'))]
    uscite_tr.append(round(sum(df_filt1_tr['Spesa A']),2))
    #PRESTITI
    df_filt1_pr=fl_st[(fl_st['A']==t) & (fl_st['Tipo_operazione'].str.match('P'))]
    uscite_pr.append(round(sum(df_filt1_pr['Spesa A']),2))
    #RINNOVI
    df_filt1_rn=fl_st[(fl_st['A']==t) & (fl_st['Tipo_operazione'].str.match('R'))]
    uscite_rn.append(round(sum(df_filt1_rn['Spesa A']),2))
    #SVINCOLATI RESCISSIONI
    df_filt1_sv=fl_st[(fl_st['A']==t) & (fl_st['Tipo_operazione'].str.match('S'))]
    uscite_sv.append(round(sum(df_filt1_sv['Spesa A']),2))
    df_filt1_c=fl_st[fl_st['A']==t]
    contracts.append(round(sum(df_filt1_c['Costo contratto']),2))
    df_voti_stip=tab_voti[(tab_voti['A']==t) & (pd.to_datetime(tab_voti['Data'])>date(2019,7,1)) & (pd.to_datetime(tab_voti['Data'])<date(2020,7,1))]
    stip.append(round(sum(df_voti_stip['Stipendio']),2))
    squad.append(t)
    quota_p.append(40)

spese=pd.DataFrame({'Squadra':squad,'Quota':quota_p,'Definitivi':uscite_tr,'Prestiti':uscite_pr,
              'Rinnovi':uscite_rn,'Svincoli':uscite_sv,'Contratti':contracts,'Stipendi':stip,
              'Totale':[sum(i) for i in zip(quota_p,uscite_tr,uscite_pr,uscite_rn,uscite_sv,contracts,stip)]})
entrate=pd.DataFrame({'Squadra':squad,'Trasferimenti':entrate_tr,'Indennizzi':entrate_in,'Premi':premi,
                      'Totale':[sum(i) for i in zip(entrate_tr,entrate_in,premi)]})

spese.to_excel(r'C:\Users\user\Desktop\Fanta dati db\per tablo\spese.xlsx',index=None,header=True)
entrate.to_excel(r'C:\Users\user\Desktop\Fanta dati db\per tablo\entrate.xlsx',index=None,header=True)


free_ag=tab_voti[(tab_voti['Giornata']>=3) & (pd.isnull(tab_voti['A']))]
free_agts=free_ag.groupby(by=['Nome','Ruolo'],as_index=False).agg({'Titolarita':'count','Gf':'sum','Rf':'sum','Ass':'sum','Gs':'sum','Rp':'sum','Rs':'sum','PI':'sum','Au':'sum','Amm':'sum','Esp':'sum','Voto':'mean','FV':'mean'})
mercato.columns=['Data op','Venditore','Acquirente','Nome','Spesa','Incasso','Tipo op','Costo Contr','Fine Prestaz']
mercato['Data op']=[pd.to_datetime(x).date() for x in mercato['Data op']]
mercato['Fine Prestaz']=[pd.to_datetime(x).date() for x in mercato['Fine Prestaz']]
mercato['Spesa']=['€{:,.2f}'.format(x) for x in mercato['Spesa']]
mercato['Incasso']=['€{:,.2f}'.format(x) for x in mercato['Incasso']]
mercato['Costo Contr']=['€{:,.2f}'.format(x) for x in mercato['Costo Contr']]


def classifica(anno,ngini=1,ngfin=36):
    sc,gc,vc,nc,pc,gfc,gsc,pntc=[],[],[],[],[],[],[],[]
    st,gt,vt,nt,pt,gft,gst,pntt=[],[],[],[],[],[],[],[]
    played=partite[pd.notnull(partite['Gol casa'])]
    played['Risultato']=[str(int(x))+'-'+str(int(y)) for x,y in zip(played['Gol casa'],played['Gol tras'])]
    tbd=partite[pd.isnull(partite['Gol casa'])]
    m=max(played['Giornata'])
    filty=played[(played['Stagione']==anno) & (played['Giornata']>=ngini) & (played['Giornata']<=ngfin)]
    l1=list(filty['Sq casa'])+(list(filty['Sq tras']))
    squad=list(set(l1))
    for i in squad:
        casa=filty[filty['Sq casa']==i]
        vc.append(sum(casa['Gol casa']>casa['Gol tras']))
        nc.append(sum(casa['Gol casa']==casa['Gol tras']))
        pc.append(sum(casa['Gol casa']<casa['Gol tras']))
        gfc.append(sum(casa['Gol casa']))
        gsc.append(sum(casa['Gol tras']))
        pntc.append(sum(casa['Pnt casa']))
        gc.append(casa.shape[0])
        sc.append(i)
        
        tras=filty[filty['Sq tras']==i]
        vt.append(sum(tras['Gol casa']<tras['Gol tras']))
        nt.append(sum(tras['Gol casa']==tras['Gol tras']))
        pt.append(sum(tras['Gol casa']>tras['Gol tras']))
        gft.append(sum(tras['Gol tras']))
        gst.append(sum(tras['Gol casa']))
        pntt.append(sum(tras['Pnt tras']))
        gt.append(tras.shape[0])
        st.append(i)
        
    pnc=[x+y for x,y in zip(nc,[3*x for x in vc])]
    pnt=[x+y for x,y in zip(nt,[3*x for x in vt])]

    cl_casa=pd.DataFrame({'Squadra':sc,'Punti':pnc,'G':gc,'W':vc,'D':nc,'L':pc,'GF':gfc,'GS':gsc,'P Glob':pntc})
    cl_trasferta=pd.DataFrame({'Squadra':st,'Punti':pnt,'G':gt,'W':vt,'D':nt,'L':pt,'GF':gft,'GS':gst,'P Glob':pntt})
    
    cl_casa=cl_casa.sort_values(by=['Punti'], ascending=False)
    cl_trasferta=cl_trasferta.sort_values(by=['Punti'], ascending=False)
    
    
    cla=pd.concat([cl_casa, cl_trasferta]).groupby(['Squadra'], as_index=False)[['Punti','G','W','D','L','GF','GS','P Glob']].sum()  
    cla=cla.sort_values(by=['Punti','P Glob'], ascending=False)
    cla.reset_index(drop=True,inplace=True)
    return [cla, played[played['Giornata']==m][['Sq casa','Sq tras','Risultato','Pnt casa','Pnt tras']], tbd[tbd['Giornata']==m+1][['Sq casa','Sq tras']]]

def classifica_cup(anno,ngini=1,ngfin=10):
    cla_both=[]
    played=coppa[pd.notnull(coppa['Gol casa'])]
    played['Risultato']=[str(int(x))+'-'+str(int(y)) for x,y in zip(played['Gol casa'],played['Gol tras'])]
    tbd=coppa[pd.isnull(coppa['Gol casa'])]
    m=max(played['Giornata'])
    for group in ['A','B']:
        sc,gc,vc,nc,pc,gfc,gsc,pntc=[],[],[],[],[],[],[],[]
        st,gt,vt,nt,pt,gft,gst,pntt=[],[],[],[],[],[],[],[]
        filty=played[(played['Stagione']==anno) & (played['Giornata']>=ngini) & (played['Giornata']<=ngfin) & (played['Gruppo']==group)]
        l1=list(filty['Sq casa'])+(list(filty['Sq tras']))
        squad=list(set(l1))
        for i in squad:
            casa=filty[filty['Sq casa']==i]
            vc.append(sum(casa['Gol casa']>casa['Gol tras']))
            nc.append(sum(casa['Gol casa']==casa['Gol tras']))
            pc.append(sum(casa['Gol casa']<casa['Gol tras']))
            gfc.append(sum(casa['Gol casa']))
            gsc.append(sum(casa['Gol tras']))
            pntc.append(sum(casa['Pnt casa']))
            gc.append(casa.shape[0])
            sc.append(i)
            
            tras=filty[filty['Sq tras']==i]
            vt.append(sum(tras['Gol casa']<tras['Gol tras']))
            nt.append(sum(tras['Gol casa']==tras['Gol tras']))
            pt.append(sum(tras['Gol casa']>tras['Gol tras']))
            gft.append(sum(tras['Gol tras']))
            gst.append(sum(tras['Gol casa']))
            pntt.append(sum(tras['Pnt tras']))
            gt.append(tras.shape[0])
            st.append(i)
            
        pnc=[x+y for x,y in zip(nc,[3*x for x in vc])]
        pnt=[x+y for x,y in zip(nt,[3*x for x in vt])]
    
        cl_casa=pd.DataFrame({'Squadra':sc,'Punti':pnc,'G':gc,'W':vc,'D':nc,'L':pc,'GF':gfc,'GS':gsc,'P Glob':pntc})
        cl_trasferta=pd.DataFrame({'Squadra':st,'Punti':pnt,'G':gt,'W':vt,'D':nt,'L':pt,'GF':gft,'GS':gst,'P Glob':pntt})
        
        cl_casa=cl_casa.sort_values(by=['Punti'], ascending=False)
        cl_trasferta=cl_trasferta.sort_values(by=['Punti'], ascending=False)
        
        
        cla=pd.concat([cl_casa, cl_trasferta]).groupby(['Squadra'], as_index=False)[['Punti','G','W','D','L','GF','GS','P Glob']].sum()  
        cla=cla.sort_values(by=['Punti','P Glob'], ascending=False)
        cla.reset_index(drop=True,inplace=True)
        cla_both.append(cla)
    return [cla_both,played[played['Giornata']==m][['Gruppo','Sq casa','Sq tras','Risultato','Pnt casa','Pnt tras']], tbd[tbd['Giornata']==m+1][['Gruppo','Sq casa','Sq tras']]]




#funzione per fare le tabelle
def generate_table(df):
    return dbc.Table( [html.Tr([html.Th(col) for col in df.columns])]+
                        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(df.shape[0])]
            ,bordered=True)

def generate_cards(him,squad,hsq,pre,ds,mr):
    return dbc.Card([dbc.CardImg(src=him,top=True),
             dbc.CardBody(dbc.CardLink(squad,href=hsq)),
             html.H5('Organigramma:'),
             html.Br(),
             html.P('Presidente ',style={'font-weight': 'bold'}),html.P(pre),
             html.Br(),
             html.P('DS ',style={'font-weight': 'bold'}),html.P(ds),
             html.Br(),
             html.P('Mister ',style={'font-weight': 'bold'}),html.P(mr)
            ]) 
def generate_lo_sq(squad,n):
    return [html.H1(squad,id='nome-'+n,title=squad),
                    html.H3('Rosa Attuale'),
                    html.Div(id='squad-'+n),
                    html.Br(),
                    html.H3('Mercato'),
                    dbc.FormGroup([
                    dbc.Label('Sessioni'),
                    dbc.RadioItems(id='sessioni-'+n,options=[{'label':'lug-dic 19','value':'est19'},
                                                           {'label':'gen-giu 20','value':'inv20'}
                                                            ],value='est19',inline=True)
                    ]),
                    dbc.Row([
                            dbc.Col([html.H6('Acquisti'),
                            html.Div(id='acquisti-'+n)
                            ]),
                            dbc.Col([
                            html.H6('Cessioni'),
                            html.Div(id='cessioni-'+n)
                            ])
                    ]),
                    html.H3('Situazione economica'),
                    dbc.Row([ 
                            dbc.Col([
                            dcc.Graph(id='pie-entrate-'+n)]),
                            dbc.Col([
                            dcc.Graph(id='pie-uscite-'+n)])
                            #dcc.Graph(id='line-01')
                            ]),
                    html.Br(),
                    dcc.Link('Home',href='/'),
                    html.Br(),
                    dcc.Link('Squadre',href='/team')]
    
#bootstrap
FantaPy=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

url_bar=dbc.Container([dcc.Location(id='url',refresh=False),
                  html.Div(id='page-content')
        ])

# **** PRIMA PAGINA LAYOUT ****
index_page = dbc.Container(style={'background-image':'url("/assets/calcio.jpeg")',
                             'background-repeat': 'no-repeat',
                              'background-position': 'center',
                              'background-size':'100% 100%'
                              },
    children=[html.H1('FantaTim Manager 2k20',style={'color':'purple','fontSize':150,'font-family':'Trebuchet MS','textAlign':'center'}),
              html.H3('Il fantacalcio come non lo avete mai visto',style={'fontSize':50,'font-family':'roboto','textAlign':'center','background-color':'white'}),
    dbc.Nav([dbc.NavItem(dbc.NavLink('Le squadre', href='/team',active=True)),   
                dbc.NavItem(dbc.DropdownMenu([dbc.DropdownMenuItem('2019-2020',header=True),
                                              dbc.DropdownMenuItem('Campionato',href='/1920league'),
                                              dbc.DropdownMenuItem('Coppa FTim',href='/1920cup'),
                                              dbc.DropdownMenuItem(divider=True)
                                              #dbc.DropdownMenuItem('2020-2021',header=True),dbc.DropdownMenuItem('Campionato'),dbc.DropdownMenuItem('Coppa FTim'),dbc.DropdownMenuItem('Champions League'),dbc.DropdownMenuItem('Europa League'),dbc.DropdownMenuItem('Birra Moretti')
                                              #dbc.DropdownMenuItem(divider=True)
                                              ]
                                              , label='Stagioni',nav=True)),
               dbc.NavItem(dbc.NavLink('Statistiche',href='/stats',active=True)),
               dbc.NavItem(dbc.NavLink('Trasferimenti',href='/market',active=True)),
               dbc.NavItem(dbc.NavLink('Albo d\'oro',href='/palmares',active=True))],pills=True)
                ])    

# **** lE SQUADRE **** 
p1=dbc.Container([html.H1('Le Squadre'), dbc.CardColumns([
        generate_cards('/assets/aelogo.png','Aquile Estensi','/team/aquile-estensi','Steven Bradbury','Arrigo Sacchi','Eziolino Capuano')
       ,generate_cards('/assets/agglogo.png','Agghiaggiande','/team/agghiaggiande','Alessandro Del Piero','Michel Platini','Antonio Conte')
       ,generate_cards('/assets/cimlogo.png','Cimamori la Verace','/team/cimamori-la-verace','Prince George','Joey Barton','Peter Crouch')
       ,generate_cards('/assets/dflogo.png','Diavoli Felsinei','/team/diavoli-felsinei','Pierluigi Pardo','Fabio Caressa','Antonio Cassano')
       ,generate_cards('/assets/dorlogo.png','Doria Emiliana','/team/doria-emiliana','Yonghong Li','Massimiliano Mirabelli','Gennaro Gattuso')
       ,generate_cards('/assets/lalogo.png','Los Angeles Showtime','/team/los-angeles-showtime','Erick Thohir','Marco Branca','Marco Materazzi')
       ,generate_cards('/assets/parlogo.png','Parter','/team/parter','Luciano Gaucci','Pantaleo Corvino','Serse Cosmi')
       ,generate_cards('/assets/tllogo.jpeg','The Lumberjacks','/team/the-lumberjacks','Sebastian Kurz','Herbert Prohaska','Marko Arnautovic')
       ,generate_cards('/assets/vanlogo.png','Vanndoria','/team/vanndoria','Lorenzo Vannini','Giampiero Ventura','Bernardo Corradi')
       ,generate_cards('/assets/zvlogo.png','Zena Viola','/team/zena-viola','Jair Bolsonero','Paolo Bargiggia','Daniele Adani')
       ]),
                    html.Br(),
                    dcc.Link('Home',href='/')
                    ])

aqes=dbc.Container(generate_lo_sq('Aquile Estensi','01'))
aggh=dbc.Container(generate_lo_sq('Agghiaggiande','02'))
cima=dbc.Container(generate_lo_sq('Cimamori la Verace','03'))
dife=dbc.Container(generate_lo_sq('Diavoli Felsinei','04'))
doel=dbc.Container(generate_lo_sq('Doria Emiliana','05'))
lash=dbc.Container(generate_lo_sq('Los Angeles Showtime','06'))    
part=dbc.Container(generate_lo_sq('Parter','07'))
thel=dbc.Container(generate_lo_sq('The Lumberjacks','08'))
vann=dbc.Container(generate_lo_sq('Vanndoria','09'))
zevi=dbc.Container(generate_lo_sq('Zena Viola','10'))

# *** CLASSIFICA E RISULTATI    
p2=dbc.Container([html.Div([html.H1('Campionato 2019-2020',id='season',title='2019-20'),
                              html.H5('Classifica'),
                            html.Div(id='rank'),
                            dbc.FormGroup([html.Br(),
                            html.H5('Ultima giornata:'),
                            html.Div(id='last-gio'),
                            html.H5('Prossima giornata:'),
                            html.Div(id='next-gio')
                            ])
                    ],style={'columnCount': 2}),
                    html.Br(),
                    dcc.Link('Home',href='/')
                    ])

p2a=dbc.Container([html.Div([html.H1('Coppa 2019-2020 - Girone A',id='cup-A',title='2019-20'),
                              html.H5('Classifica'),
                            html.Div(id='rank-A'),
                            dbc.FormGroup([html.Br(),
                            html.H5('Ultima giornata:'),
                            html.Div(id='last-gio-A'),
                            html.H5('Prossima giornata:'),
                            html.Div(id='next-gio-A')
                            ])
                    ],style={'columnCount': 2}),
                    html.Br(),
                    dcc.Link('Home',href='/')
                    ])
                
p2b=dbc.Container([html.Div([html.H1('Coppa 2019-2020 - Girone B',id='cup-B',title='2019-20'),
                              html.H5('Classifica'),
                            html.Div(id='rank-B'),
                            dbc.FormGroup([html.Br(),
                            html.H5('Ultima giornata:'),
                            html.Div(id='last-gio-B'),
                            html.H5('Prossima giornata:'),
                            html.Div(id='next-gio-B')
                            ])
                    ],style={'columnCount': 2}),
                    html.Br(),
                    dcc.Link('Home',href='/')
                    ])
                
pfin=dbc.Container([html.H1('Finale coppa 2019-2020',id='final-c',title='2019-20')
        ])
                
pcup=html.Div([
    dbc.Tabs([ dbc.Tab(p2a,label='Gruppo A',tab_id='gr-a'),
                dbc.Tab(p2b,label='Gruppo B',tab_id='gr-b'),
                dbc.Tab(pfin,label='Finale',tab_id='fin-cup')
            ],id='tabs-cup',active_tab='gr-a')
            ])
 
# *** STATISTICHE
p3a=dbc.Container([html.H3('Stagione 2019-2020',title='2019-20',id='st-ov'),
        html.H5('Regressione punti campo/punti globali'),
        dcc.Graph(id='regr'),
        html.Br(),
        html.H5('La controclassifica - The Gay Index'),
        html.Div(id='gay'),
        dcc.Link('Home',href='/')           
        ])                
                
p3b=dbc.Container([
        dcc.Dropdown(id='list_sq', options=[{'label':i,'value':i} for i in sorted(set(partite['Sq casa']))], value='Agghiaggiande'),
        html.H5('Progressione punti'),
        dcc.Graph(id='andamento'), #hovertext
        dbc.Row([dbc.Col([
                    html.H6('Nazionalità'),
                    dcc.Graph(id='ana_sq_naz')
                    ]),
                dbc.Col([
                    html.H6('Età'),
                    dcc.Graph(id='ana_sq_eta')
                    ])
                ]),
        dbc.Row([dbc.Col([
                    html.H6('Stipendi più alti'),
                    html.Div(id='high-stip')
                ]),
                dbc.Col([
                    html.H6('Giocatori più usati'),
                    html.Div(id='stakanov')
                ]),
                dbc.Col([
                    html.H6('Le rogne'),
                    html.Div(id='mannaggia')
                ])
                ]),
        html.Br(),
        dcc.Link('Home',href='/')                    
        ])     
               
p3c=dbc.Container([
      dcc.Dropdown(id='list_pl', options=[{'label':i,'value':i} for i in sorted(set(mercato['Nome']))], value='ACERBI'),
      html.H5('Andamento voti e FM'),
      dcc.Graph(id='voti'),
      html.H5('Carriera'),
      html.Div(id='carriera'),
      html.Br(),
      dcc.Link('Home',href='/')             
        ])       
                
p3=html.Div([
    dbc.Tabs([ dbc.Tab(p3a,label='Overall',tab_id='stat-tot'),
                dbc.Tab(p3b,label='Per squadra',tab_id='stat-sq'),
              dbc.Tab(p3c,label='Per giocatore',tab_id='stat-play')
            ],id='tabs',active_tab='stat-sq')
            ])
                
p4b=dbc.Container([
                  html.H3('Lista svincolati'),
                  html.Div([
                  dash_table.DataTable(id='free-agent',columns=[{
                          'name':i,'id':i} for i in free_agts.columns],
                            data=free_agts.to_dict('records'),
                            filter_action='native')
                    ],id='filt-df-adv'),
                  html.Br(),
                  dcc.Link('Home',href='/')
        ])

p4a=dbc.Container([html.H3('Movimenti di mercato'), 
                  html.Div([
                  dash_table.DataTable(id='mov-mark',columns=[{
                          'name':i,'id':i} for i in mercato.columns],
                            data=mercato.to_dict('records'),
                            filter_action='native')
                    ],id='filt-df'),
                html.Br(),
                 dcc.Link('Home',href='/')            
                ])

p4=html.Div([
    dbc.Tabs([ dbc.Tab(p4a,label='Mercato',tab_id='mk'),
                dbc.Tab(p4b,label='Svincolati',tab_id='fa')
            ],id='tabs-mk',active_tab='mk')
            ])

def serve_layout():
    if flask.has_request_context():
        return url_bar
    return dbc.Container([
        url_bar,
        index_page,
       p1,
       aqes,aggh,cima,dife,doel,lash,part,thel,vann,zevi,
       p2,pcup,p3,p4
    ])  
    
FantaPy.layout=serve_layout
    
@FantaPy.callback(Output('page-content','children'),
              [Input('url','pathname')]) 
def display_page(pathname):
    if pathname == "/team":
        return p1
    elif pathname == "/team/aquile-estensi":
        return aqes
    elif pathname == "/team/agghiaggiande":
        return aggh
    elif pathname == "/team/cimamori-la-verace":
        return cima
    elif pathname == "/team/diavoli-felsinei":
        return dife
    elif pathname == "/team/doria-emiliana":
        return doel
    elif pathname == "/team/los-angeles-showtime":
        return lash
    elif pathname == "/team/parter":
        return part
    elif pathname == "/team/the-lumberjacks":
        return thel
    elif pathname == "/team/vanndoria":
        return vann
    elif pathname == "/team/zena-viola":
        return zevi
    elif pathname == "/1920league":
        return p2
    elif pathname == "/1920cup":
        return pcup
    elif pathname == "/stats":
        return p3
    elif pathname == "/market":
        return p4
#    elif pathname == "/palmares":
#        return p5
    else:
        return index_page

for i in ['01','02','03','04','05','06','07','08','09','10']:    
    @FantaPy.callback([Output('squad-'+i,'children'),
                 Output('acquisti-'+i,'children'),
                  Output('cessioni-'+i,'children'),
                  Output('pie-entrate-'+i,'figure'),
                  Output('pie-uscite-'+i,'figure')],
                  [Input('nome-'+i,'title'),
                   Input('sessioni-'+i,'value')])
    def tab_sq(squadra,sess):
        d=ana_gio[ana_gio['Squadra']==squadra]
        d['Fine P']=[x.date() for x in d['Fine prestazione']]
        d['Data Nascita']=[x.date() for x in d['Data nascita']]
        d['Value €']=['€{:,.2f}'.format(x) for x in d['Valore']]
        d=d[['Nome completo','Ruolo','Data Nascita','Luogo nascita','Nazionalità','Età','Tipo contratto','Fine P','Value €']]  
        if sess == 'est19':
            ac=mercato[(mercato['Data op']>date(2019,7,1)) & (mercato['Data op']<date(2020,1,1)) & (mercato['Acquirente']==squadra)]
            ce=mercato[(mercato['Data op']>date(2019,7,1)) & (mercato['Data op']<date(2020,1,1)) & (mercato['Venditore']==squadra)]
        else:
            ac=mercato[(mercato['Data op']>=date(2020,1,1)) & (mercato['Data op']<date(2020,7,1)) & (mercato['Acquirente']==squadra)]
            ce=mercato[(mercato['Data op']>=date(2020,1,1)) & (mercato['Data op']<date(2020,7,1)) & (mercato['Venditore']==squadra)]
        tab_ac=ac[['Data op','Nome','Venditore','Spesa','Tipo op']]
        tab_ce=ce[['Data op','Nome','Acquirente','Incasso','Tipo op']]
        
        ent=entrate[entrate['Squadra']==squadra].values.tolist()[0][1:4]
        usc=spese[spese['Squadra']==squadra].values.tolist()[0][1:8]
        
        fig_en=go.Figure(data=[go.Pie(labels=entrate.columns[1:4].tolist(), values=ent, hole=.3)])
        fig_en.update_layout(title_text='Entrate',annotations=[dict(text='€{:,.2f}'.format(entrate[entrate['Squadra']==squadra].values.tolist()[0][4]),x=0.5,y=0.5,font=dict(color='green'),showarrow=False,font_size=18)])
        
        fig_us=go.Figure(data=[go.Pie(labels=spese.columns[1:8].tolist(), values=usc, hole=.3)])
        fig_us.update_layout(title_text='Spese',annotations=[dict(text='- '+'€{:,.2f}'.format(spese[spese['Squadra']==squadra].values.tolist()[0][8]),x=0.5,y=0.5,font=dict(color='red'),showarrow=False,font_size=18)])
        
        
        return [generate_table(d),generate_table(tab_ac),generate_table(tab_ce),fig_en,fig_us]

@FantaPy.callback([Output('rank','children'),
                   Output('last-gio','children'),
                   Output('next-gio','children')],
                  [Input('season','title')])
def campionato(stagione):
    return [generate_table(classifica(stagione)[0]),
            generate_table(classifica(stagione)[1]),
            generate_table(classifica(stagione)[2])]
    
@FantaPy.callback([Output('rank-A','children'),
                   Output('last-gio-A','children'),
                   Output('next-gio-A','children')],
                  [Input('cup-A','title')])
def cup_a(stagione):
    return [generate_table(classifica_cup(stagione)[0][0]),
            generate_table(classifica_cup(stagione)[1][classifica_cup(stagione)[1]['Gruppo']=='A'].drop('Gruppo',axis=1)),
            generate_table(classifica_cup(stagione)[2][classifica_cup(stagione)[2]['Gruppo']=='A'].drop('Gruppo',axis=1))]    

@FantaPy.callback([Output('rank-B','children'),
                   Output('last-gio-B','children'),
                   Output('next-gio-B','children')],
                  [Input('cup-B','title')])
def cup_b(stagione):
    return [generate_table(classifica_cup(stagione)[0][1]),
            generate_table(classifica_cup(stagione)[1][classifica_cup(stagione)[1]['Gruppo']=='B'].drop('Gruppo',axis=1)),
            generate_table(classifica_cup(stagione)[2][classifica_cup(stagione)[2]['Gruppo']=='B'].drop('Gruppo',axis=1))]     

@FantaPy.callback([Output('regr','figure'),
                   Output('gay','children')],
                  [Input('st-ov','title')])
def regress(stag):
    match=partite[pd.notnull(partite['Gol casa'])]
    df=match[match['Stagione']==stag]
    df.reset_index(drop=True,inplace=True)
    exp_p=[]
    df_casa=df[['Giornata','Sq casa','Gol casa']]
    df_casa.columns=['Giornata','Squadra','Gol']
    df_tras=df[['Giornata','Sq tras','Gol tras']]
    df_tras.columns=['Giornata','Squadra','Gol']
    df=pd.concat([df_casa,df_tras]).sort_values('Giornata')
    df.reset_index(drop=True,inplace=True)
    for i in range(df.shape[0]):
        gf=df.iloc[i,2]
        gio=df.iloc[i,0]
        dfdrop=df.drop(i)
        rag=dfdrop[dfdrop['Giornata']==gio].groupby('Gol').count()['Squadra']
        cal_parz=[]
        for k in range(len(rag)):
            if gf>rag.index[k]:
                cal_parz.append((rag[k]/9)*3)
            elif gf==rag.index[k]:
                cal_parz.append(rag[k]/9)
        exp_p.append(sum(cal_parz))
    df_arr=pd.concat([df,pd.DataFrame({'Exp Pnt':exp_p})],axis=1)
    dagg=df_arr.groupby('Squadra',as_index=False).agg({'Exp Pnt':'sum'})
    dagg['Exp Pnt']=round(dagg['Exp Pnt'],0)
    df_arr1=pd.merge(dagg,classifica(stag)[0][['Squadra','Punti']],on='Squadra',how='left')
    df_arr1['Gay Index']=[x-y for x,y in zip(df_arr1['Punti'],df_arr1['Exp Pnt'])]
    df_arr1=df_arr1.sort_values(by=['Exp Pnt'],ascending=False)        
    return [px.scatter(classifica('2019-20')[0], x='P Glob', y='Punti',
	         size='GF',hover_name='Squadra',trendline='ols'),
            generate_table(df_arr1)]

@FantaPy.callback([Output('andamento','figure'),
                   Output('ana_sq_naz','figure'),
                   Output('ana_sq_eta','figure'),
                   Output('high-stip','children'),
                   Output('stakanov','children'),
                   Output('mannaggia','children')],
                  [Input('list_sq','value')])
def stat_team(team):
    ec,et=[],[]
    match=partite[pd.notnull(partite['Gol casa'])]
    casa=match[match['Sq casa']==team].rename(columns={'Pnt casa':'P Glob'}).drop('Pnt tras',axis=1)
    tras=match[match['Sq tras']==team].rename(columns={'Pnt tras':'P Glob'}).drop('Pnt casa',axis=1)
    tras.reset_index(drop=True,inplace=True)
    casa.reset_index(drop=True,inplace=True)
    for i in range(casa.shape[0]):
        if casa.iloc[i,4]>casa.iloc[i,5]:
            ec.append('W')
        elif casa.iloc[i,4]==casa.iloc[i,5]:
            ec.append('D')
        else:
            ec.append('L')
    
    for i in range(tras.shape[0]):
        if tras.iloc[i,4]<tras.iloc[i,5]:
            et.append('W')
        elif tras.iloc[i,4]==tras.iloc[i,5]:
            et.append('D')
        else:
            et.append('L')
                        
    casa=pd.concat([casa,pd.DataFrame({'Esito':ec})],axis=1)
    tras=pd.concat([tras,pd.DataFrame({'Esito':et})],axis=1)
    df=pd.concat([casa,tras]).sort_values(['Giornata'])
    df.reset_index(drop=True,inplace=True)
    if df['Esito'][0]=='W':
        p_acc=[3]
    elif df['Esito'][0]=='D':
        p_acc=[1]
    else:
        p_acc=[0]
    for i in range(1,df.shape[0]):
        if df['Esito'][i]=='W':
            p_acc.append(p_acc[i-1]+3)
        elif df['Esito'][i]=='D':
            p_acc.append(p_acc[i-1]+1)
        else:
            p_acc.append(p_acc[i-1])
    df=pd.concat([df,pd.DataFrame({'P acc':p_acc})],axis=1)
    
    fig1=make_subplots(specs=[[{'secondary_y':True}]])
    fig1.add_trace(go.Scatter(x=df['Giornata'],y=df['P Glob']),secondary_y=False)
    fig1.add_trace(go.Scatter(x=df['Giornata'],y=df['P acc'],fill='tozeroy'),secondary_y=True)
    fig1.add_trace(go.Scatter(x=df['Giornata'].unique().tolist(),y=[np.nanmean(df['P Glob'])]*df['Giornata'].max(),mode='lines',line=dict(color='RoyalBlue',dash='dashdot')),secondary_y=False)
    fig1.add_annotation(go.layout.Annotation(x=0,y=0.5,text='MP: '+str(round(np.nanmean(df['P Glob']),2)),bgcolor='#ff7f0e',opacity=0.8,showarrow=False))
    fig1.update_xaxes(title_text='Giornata')
    fig1.update_yaxes(title_text='Punti Globali',secondary_y=False)
    fig1.update_yaxes(title_text='Punti',secondary_y=True)
        
    df1=ana_gio[ana_gio['Squadra']==team]
    df1_agg=df1.groupby('Nazionalità',as_index=False).agg({'Nome':'count'})
    df1_agg.columns=['Nazionalità','N gio']
    fig_2=go.Figure(data=[go.Pie(labels=df1_agg['Nazionalità'], values=df1_agg['N gio'])])
    fig_2.update_layout(title_text='Nazionalità squadra')
    
    
    df2=ana_gio[ana_gio['Squadra']==team]
    df2_agg=df2.groupby(pd.cut(df2['Età'],bins=np.array([15,20,23,26,29,32,35,38,41,44])),as_index=False).count()
    fig_3=px.bar(df2_agg,x=['<20','20-23','23-26','26-29','29-32','32-35','35-38','38-41','41-44'],y='Nome')
    fig_3.add_shape(go.layout.Shape(type='line',x0=np.nanmean(df2['Età']),x1=np.nanmean(df2['Età']),y0=0,y1=df2_agg['Nome'].max()))
    fig_3.update_layout(title_text='Distribuzione età',yaxis_title='Count')
    fig_3.update_xaxes(title_text='Età')
    fig_3.update_yaxes(title_text='Frequency')
    
    df3=tab_voti[tab_voti['A']==team]
    df3=df3.groupby('Nome',as_index=False).agg({'Stipendio':'sum'})
    df3['Stipendio']=['€{:,.2f}'.format(x) for x in df3['Stipendio']]
    df3=df3.sort_values(['Stipendio'],ascending=False).iloc[:10,:]
    
    df4=tab_voti[tab_voti['A']==team]
    df4=df4.groupby('Nome',as_index=False).agg({'Titolarita':'sum'})
    df4=df4.sort_values(['Titolarita'],ascending=False).iloc[:10,:]

    df5=tab_voti[(tab_voti['A']==team) & (tab_voti['Titolarita']==0)]
    df5=df5[['Nome','Giornata','FV']].sort_values('FV',ascending=False).iloc[:10,:]
    
    return[fig1,fig_2,fig_3,generate_table(df3),generate_table(df4),generate_table(df5)]

@FantaPy.callback([Output('voti','figure'),
                   Output('carriera','children')],
                  [Input('list_pl','value')])
def stat_pla(player):
    df=tab_voti[tab_voti['Nome']==player]
    fig4=go.Figure()
    fig4.add_trace(go.Scatter(x=df['Giornata'],y=df['Voto'],fill='tozeroy'))
    fig4.add_trace(go.Scatter(x=df['Giornata'],y=df['FV'],fill='tonexty'))
    fig4.add_trace(go.Scatter(x=df['Giornata'].unique().tolist(),y=[np.nanmean(df['Voto'])]*df['Giornata'].max(),mode='lines',line=dict(color='RoyalBlue',dash='dashdot')))
    fig4.add_trace(go.Scatter(x=df['Giornata'].unique().tolist(),y=[np.nanmean(df['FV'])]*df['Giornata'].max(),mode='lines',line=dict(color='red',dash='dash')))
    fig4.add_annotation(go.layout.Annotation(x=0.1,y=0.5,text='FV: '+str(round(np.nanmean(df['FV']),2)),bgcolor='#ff7f0e',opacity=0.8,showarrow=False))
    fig4.add_annotation(go.layout.Annotation(x=0.9,y=0.5,text='MV: '+str(round(np.nanmean(df['Voto']),2)),bgcolor='#64e6e8',opacity=0.8,showarrow=False))
    fig4.update_yaxes(title_text='Voto')
    fig4.update_xaxes(title_text='Giornata')

    carr=df.groupby('A',as_index=False).agg({'Titolarita':'sum','Gf':'sum','Rf':'sum','Ass':'sum','Gs':'sum','Rp':'sum','Rs':'sum','PI':'sum','Au':'sum','Amm':'sum','Esp':'sum','Stipendio':'sum','Voto':'mean','FV':'mean','Data':['min','max']})
    carr.columns=['Squadra','Pres','Gol F','Gol R','Ass','Gol S','Rig P','Reti S','P Inv','Aut','Amm','Esp','Stip','MV','FV','Da','A']
    carr['Stip']=['€{:,.2f}'.format(x) for x in carr['Stip']]
    carr['Da']=[pd.to_datetime(x).date() for x in carr['Da']]
    carr['A']=[pd.to_datetime(x).date() for x in carr['A']]
    return [fig4,generate_table(carr)]
 
@FantaPy.callback([Output('filt-df','children')],
                  [Input('mov-mark','data')])
def mark(rows):
    if rows is None:
        df=mercato
    else:
        df=pd.DataFrame(rows)
    return html.Div()
    
@FantaPy.callback([Output('filt-df-adv','children')],
                  [Input('free-agent','data')])
def fa(rows1):
    free_agts['Voto']=round(free_agts['Voto'],2)
    free_agts['FV']=round(free_agts['FV'],2)
    if rows1 is None:
        df1=free_agts
    else:
        df1=pd.DataFrame(rows1)        
    return html.Div()

if __name__ == "__main__":
    FantaPy.run_server()







#def graf(nome):
#    d=tab_voti[tab_voti['Nome']==nome]
#    dep=np.isfinite(d['Voto'])
#    plt.plot(d[dep]['Giornata'],d[dep]['Voto'],d[dep]['Giornata'],d[dep]['FV'],'b-',d[dep]['Giornata'],list(np.repeat(np.nanmean(d[dep]['Voto']),len(d[dep]['Voto']))),'r--',d[dep]['Giornata'],list(np.repeat(np.nanmean(d[dep]['FV']),len(d[dep]['Voto']))),'g--')
#    plt.axis([1,max(tab_voti['Giornata']),min(tab_voti['FV']),max(tab_voti['FV'])])
#    plt.text(1,np.nanmean(d[dep]['Voto'])+0.1,'MV:'+str(round(np.nanmean(d[dep]['Voto']),2)),fontweight='bold',backgroundcolor='tab:pink')
#    plt.text(max(tab_voti['Giornata'])-1.25,np.nanmean(d[dep]['FV'])+0.1,'FV:'+str(round(np.nanmean(d[dep]['FV']),2)),fontweight='bold',backgroundcolor='tab:pink')
#    plt.title(nome)

#print( voti_arr.dtypes)