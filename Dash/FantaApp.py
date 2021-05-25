# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 17:51:58 2020

@author: user
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
import dash_daq as daq
import plotly.graph_objects as go
from plotly.offline import plot
import flask
import pandas as pd
import pandasql as ps
import numpy as np
#from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
from datetime import date

voti = pd.read_excel('Voti_new.xlsx')
mercato = pd.read_excel('DBFanta.xlsx', sheet_name='Mercato')
ruolo = pd.read_excel('DBFanta.xlsx', sheet_name='Ruolo')
giocatori = pd.read_excel('DBFanta.xlsx', sheet_name='Giocatori')
quotazioni = pd.read_excel('Quotazioni_new.xlsx')
organigramma = pd.read_excel('DBFanta.xlsx', sheet_name='Organigramma')
campionato = pd.read_excel('DBFanta.xlsx', sheet_name='Campionato')
coppa = pd.read_excel('DBFanta.xlsx', sheet_name='Cup')
moduli= pd.read_excel('Moduli.xlsx', sheet_name='Schema')

giocatori['Età']=[int((date.today()-x.date()).days/365.2425) for x in giocatori['Data_nascita']]
#bandiere = dict(zip(bandiere['Stato'],bandiere['Bandiera']))
sigle = {'Aquile Estensi':'ae','Agghiaggiande':'agg','Cimamori la Verace':'cim','Diavoli Felsinei':'df','Doria Emiliana':'dor','Parter':'par','Los Angeles Showtime':'la','The Lumberjacks':'tl','Vanndoria':'van','Zena Viola':'zv'}
pos_draw={'343':{'p1':[[313,895],'pdown'],'p2':[[210,745],'pdown'],'p3':[[313,745],'pup'],'p4':[[420,745],'pdown'],'p5':[[110,465],'pup'],'p6':[[210,465],'pdown'],
                'p7':[[420,465],'pup'],'p8':[[525,465],'pdown'],'p9':[[210,185],'pdown'],'p10':[[313,185],'pup'],'p11':[[420,185],'pdown']},
         '3412':{'p1': [[313, 895], 'pdown'], 'p2': [[210, 745], 'pdown'], 'p3': [[313, 745], 'pup'], 'p4': [[420, 745], 'pdown'], 'p5': [[110, 465], 'pup'], 'p6': [[210, 465], 'pdown'],
                'p7': [[420, 465], 'pup'], 'p8': [[525, 465], 'pdown'], 'p9': [[313, 325], 'pdown'], 'p10': [[210, 185], 'pup'], 'p11': [[420, 185], 'pdown']},
         '3421':{'p1': [[313, 895], 'pdown'], 'p2': [[210, 745], 'pdown'], 'p3': [[313, 745], 'pup'], 'p4': [[420, 745], 'pdown'], 'p5': [[110, 465], 'pup'], 'p6': [[210, 465], 'pdown'],
                'p7': [[420, 465], 'pup'], 'p8': [[525, 465], 'pdown'], 'p9': [[210, 325], 'pdown'], 'p10': [[420, 325], 'pup'], 'p11': [[313, 185], 'pdown']},
         '352': {'p1': [[313, 895], 'pdown'], 'p2': [[210, 745],'pdown'], 'p3': [[313, 745],'pup'], 'p4': [[420, 745],'pdown'], 'p5': [[110, 465],'pdown'], 'p6': [[210, 465],'pup'],
                'p7': [[313, 465],'pdown'], 'p8': [[420, 465],'pup'], 'p9': [[525, 465],'pdown'], 'p10': [[210, 185],'pup'], 'p11': [[420, 185],'pdown']},
        '3511': {'p1': [[313, 895], 'pdown'], 'p2': [[210, 745], 'pdown'], 'p3': [[313, 745], 'pup'], 'p4': [[420, 745], 'pdown'], 'p5': [[110, 465],'pdown'], 'p6': [[210, 465],'pup'],
                'p7': [[313, 465],'pdown'], 'p8': [[420, 465],'pup'], 'p9': [[525, 465],'pdown'], 'p10': [[313, 325], 'pup'], 'p11': [[313, 185], 'pdown']},
        '433':  {'p1': [[313, 895], 'pdown'], 'p2': [[110, 745], 'pup'], 'p3': [[210, 745], 'pdown'], 'p4': [[420, 745], 'pup'], 'p5': [[525, 745], 'pdown'], 'p6': [[210, 465], 'pdown'],
                'p7': [[313, 465], 'pup'], 'p8': [[420, 465], 'pdown'], 'p9':[[210,185],'pdown'],'p10':[[313,185],'pup'],'p11':[[420,185],'pdown']},
        '4312':  {'p1': [[313, 895], 'pdown'], 'p2': [[110, 745], 'pup'], 'p3': [[210, 745], 'pdown'], 'p4': [[420, 745], 'pup'], 'p5': [[525, 745], 'pdown'], 'p6': [[210, 465], 'pdown'],
                'p7': [[313, 465], 'pup'], 'p8': [[420, 465], 'pdown'], 'p9': [[313, 325], 'pdown'], 'p10': [[210, 185], 'pup'], 'p11': [[420, 185], 'pdown']},
        '442': {'p1': [[313, 895], 'pdown'], 'p2': [[110, 745], 'pup'], 'p3': [[210, 745], 'pdown'], 'p4': [[420, 745], 'pup'], 'p5': [[525, 745], 'pdown'], 'p6': [[110, 465], 'pup'],
                'p7': [[210, 465], 'pdown'], 'p8': [[420, 465], 'pup'], 'p9': [[525, 465], 'pdown'], 'p10': [[210, 185], 'pup'], 'p11': [[420, 185], 'pdown']},
        '4141': {'p1': [[313, 895], 'pdown'], 'p2': [[110, 745], 'pup'], 'p3': [[210, 745], 'pdown'], 'p4': [[420, 745], 'pup'], 'p5': [[525, 745], 'pdown'], 'p6': [[110, 465], 'pdown'],
                'p7': [[210, 465], 'pup'], 'p8': [[313, 605], 'pdown'], 'p9': [[420, 465], 'pdown'], 'p10': [[525, 465], 'pup'], 'p11': [[313, 185], 'pdown']},
        '4411': {'p1': [[313, 895], 'pdown'], 'p2': [[110, 745], 'pup'], 'p3': [[210, 745], 'pdown'], 'p4': [[420, 745], 'pup'], 'p5': [[525, 745], 'pdown'], 'p6': [[110, 465], 'pdown'],
                'p7': [[210, 465], 'pup'], 'p8': [[420, 465], 'pdown'], 'p9': [[525, 465], 'pup'], 'p10': [[313, 325], 'pup'], 'p11': [[313, 185], 'pdown']},
        '4231': {'p1': [[313, 895], 'pdown'], 'p2': [[110, 745], 'pup'], 'p3': [[210, 745], 'pdown'], 'p4': [[420, 745], 'pup'], 'p5': [[525, 745], 'pdown'], 'p6': [[210, 465], 'pup'],
                'p7': [[420, 465], 'pdown'], 'p8': [[210, 325], 'pup'], 'p9': [[313, 325], 'pdown'], 'p10': [[420, 325], 'pup'], 'p11': [[313, 185], 'pdown']}}

def voti_arrk():
    m=mercato
    voti_arr=pd.merge(voti,ruolo,on=['Nome','Stagione'],how='left')
    voti_arr=voti_arr.assign(PI=0)
    voti_arr.loc[(voti_arr['Gs']==0) & (voti_arr['Ruolo']=='Por'),'PI']=1
    voti_arr['Stipendio']=voti_arr['Gf']*0.15+voti_arr['Rp']*0.15+voti_arr['Rf']*0.1+voti_arr['Ass']*0.05+voti_arr['PI']*0.05
    voti_arr.loc[pd.isnull(voti_arr['Stipendio']),'Stipendio']=0
    m['name']=m['Nome']
    sqlquery=''' 
    select * , b.A 
    from voti_arr as a 
    left join  (select A, name, Data, TP from m) as b on 
    a.Nome=b.name and a.Data between b.Data and b.TP and a.Giornata>2
    '''
    tab_voti=ps.sqldf(sqlquery,locals())
    tab_voti=tab_voti.iloc[:,1:20]
    tab_voti['FV']=tab_voti.apply(lambda x: x['Voto']+x['Gf']*3-x['Gs']+x['Rp']*3-x['Rs']*2+x['Rf']*2-x['Au']*2-x['Amm']*.5-x['Esp']+x['Ass'],axis=1)

    tab_voti.loc[(tab_voti['Voto'] == 6) & (pd.isnull(tab_voti['Gf'])), 'FV'] = 6
    tab_voti=tab_voti.drop('name',axis=1)
    return tab_voti

def anag_players(team):
    fm = mercato[(mercato['Data'] <= pd.Timestamp('today').floor('D')) & (mercato['TP'] >= pd.Timestamp('today').floor('D')) & (mercato['A']==team)]
    r = ruolo[ruolo['Stagione']==max(ruolo['Stagione'])]
    q = quotazioni[quotazioni['Stagione']==max(quotazioni['Stagione'])]
    ana1 = pd.merge(giocatori, fm[['A', 'Tipo_operazione', 'TP', 'Nome']], left_on='ID', right_on='Nome',
                    how='inner').drop('Nome_y',axis=1)
    ana2 = pd.merge(ana1, r[['Ruolo', 'Nome']], left_on='ID', right_on='Nome', how='left').drop('Nome',axis=1)
    ana_gio = pd.merge(ana2, q[['VA', 'Nome', 'VI']], left_on='ID', right_on='Nome', how='left').drop('Nome',
                                                                                                                axis=1)
    ana_gio.columns = ['Nome', 'Nome Completo', 'Data Nascita', 'Luogo Nascita', 'Nazionalità', 'Età', 'Squadra',
                       'Tipo Contratto', 'Fine Prestazione', 'Ruolo', 'Value Act', 'Value Ini']
    ana_gio['Data Nascita']=[x.date() for x in ana_gio['Data Nascita']]
    ana_gio['Fine Prestazione']=[x.date() for x in ana_gio['Fine Prestazione']]

    return ana_gio

def classifica(match, seas, gr='All'):
    if gr=='A':
        match=match[match['Gruppo']=='A']
    if gr=='B':
        match=match[match['Gruppo']=='B']    
    match=match[match['Stagione']==seas]
    match['v']=[1 if x>y else 0 for x,y in zip(match['Gol casa'],match['Gol tras'])]
    match['n']=[1 if x==y else 0 for x,y in zip(match['Gol casa'],match['Gol tras'])]
    match['p']=[1 if x<y else 0 for x,y in zip(match['Gol casa'],match['Gol tras'])]
                #casa
    dfc=match.groupby('Sq casa',as_index=False).agg({'Giornata':'count','v':'sum','n':'sum','p':'sum','Gol casa':'sum','Gol tras':'sum','Pnt casa':'sum'})
    dfc['pnt']=[3*x+y for x,y in zip(dfc['v'],dfc['n'])]
    dfc=dfc[['Sq casa','pnt','Giornata','v','n','p','Gol casa','Gol tras','Pnt casa']]
    dfc.columns=['Squadra','Pnt','Pl','W','D','L','GF','GS','P Glob']
                #trasferta
    dft=match.groupby('Sq tras',as_index=False).agg({'Giornata':'count','p':'sum','n':'sum','v':'sum','Gol tras':'sum','Gol casa':'sum','Pnt tras':'sum'})
    dft['pnt']=[3*x+y for x,y in zip(dft['p'],dft['n'])]
    dft=dft[['Sq tras','pnt','Giornata','p','n','v','Gol tras','Gol casa','Pnt tras']]
    dft.columns=['Squadra','Pnt','Pl','W','D','L','GF','GS','P Glob']
                #finale
    rank=pd.concat([dfc, dft]).groupby(['Squadra'], as_index=False)[['Pnt','Pl','W','D','L','GF','GS','P Glob']].sum()
    rank=rank.sort_values(by=['Pnt','P Glob','GF'], ascending=False)
    return rank

def contro_class(s):
    df=campionato[campionato['Stagione']==s]
    df_casa=df[['Giornata','Sq casa','Gol casa']]
    df_casa.columns=['Giornata','Squadra','Gol']
    df_tras=df[['Giornata','Sq tras','Gol tras']]
    df_tras.columns=['Giornata','Squadra','Gol']
    df=df_casa.append(df_tras).sort_values('Giornata')
    exp_p=[]
    for k in list(set(df['Giornata'])):
        dfc=df[df['Giornata']==k]
        dfc.reset_index(drop=True,inplace=True)
        for i in list(range(dfc.shape[0])):
            val_rif=dfc.iloc[i,2]
            dfd=dfc.drop(i)
            exp_p.append(3*sum(dfd['Gol']<val_rif)/9+sum(dfd['Gol']==val_rif)/9)
    df.reset_index(drop=True,inplace=True)
    df_arr=pd.concat([df,pd.DataFrame({'Exp Pnt':exp_p})],axis=1)
    dagg=df_arr.groupby('Squadra',as_index=False).agg({'Exp Pnt':'sum'})
    dagg['Exp Pnt']=[int(x) for x in dagg['Exp Pnt']]
    return dagg    

def b11(s,g,t='All'):
    v=voti_arrk()
    if t=='All':
        v=v[(v['Giornata']==g) & (v['Stagione']==s)][['Nome','Ruolo','FV']]
    else:
        v=v[(v['Giornata']==g) & (v['Stagione']==s) & (v['A']==t)][['Nome','Ruolo','FV']]
    lg_sort=v.sort_values('FV',ascending=False)
    lg_sort=lg_sort[pd.notnull(lg_sort['FV'])]
    lg_sort.reset_index(drop=True,inplace=True)
    f_df=pd.DataFrame()
    for modul in list(set(moduli['Modulo'])):
        modulis=moduli[moduli['Modulo']==modul]
        df=pd.merge(lg_sort,modulis,on='Ruolo',how='left')
        df['Pos']=df.iloc[:,4:].apply(lambda x: x.index[x.astype(bool)].tolist(), 1)
        p,n,lun=[],[],[]
        for i in list(range(df.shape[0])):
            for l in df.iloc[i,15]:
                p.append(l)
                n.append(df.iloc[i,0])
                lun.append(len(df.iloc[i,15]))
        riep=pd.DataFrame({'Pos':p,'N':n,'Len':lun})
        f2=pd.merge(riep,df.iloc[:,:4],left_on='N',right_on='Nome',how='left')
        f2=f2.drop('N',axis=1).drop('Len',axis=1).sort_values('FV',ascending=False)
        Bsel=pd.merge(f2,f2.groupby('Pos',as_index=False).agg({'FV':'max','Nome':'first'}),on=['Pos','FV','Nome'],how='right')
        Bsel['ID']=[x+y for x,y in zip(Bsel['Pos'],Bsel['Nome'])]
        f2['ID']=[x+y for x,y in zip(f2['Pos'],f2['Nome'])]
        sub=f2[~f2['ID'].isin(Bsel['ID'])]
        while Bsel.shape[0]<11:
            Bsel.loc[Bsel.shape[0]]=['','','',0,Bsel.iloc[0,4],'']
        count_dup = sum(pd.value_counts(list(filter(None,Bsel['Nome']))).to_frame().reset_index()[0]!=1)
        while count_dup!=0:
            for nn in list(filter(None,list(set(Bsel['Nome'])))):
                h=Bsel[Bsel['Nome']==nn].shape[0]
                while h>1:
                    selec=sub[sub['Pos'].isin(Bsel.loc[Bsel['Nome']==nn,'Pos'])].head(1)
                    if selec.shape[0]>0:
                        Bsel[Bsel['Pos']==selec.iloc[0,0]]=selec.iloc[0,0],selec.iloc[0,1],selec.iloc[0,2],selec.iloc[0,3],selec.iloc[0,4],selec.iloc[0,5]
                    else:
                        Bsel=Bsel[~Bsel['Pos'].isin(Bsel.loc[Bsel['Nome']==nn,'Pos'].head(1))]
                        Bsel.reset_index(drop=True,inplace=True)
                        Bsel.loc[Bsel.shape[0]]=['','','',0,Bsel.iloc[0,4],'']
                    sub=sub[~sub['ID'].isin(selec['ID'])]
                    h=h-1
            count_dup = sum(pd.value_counts(list(filter(None,Bsel['Nome']))).to_frame().reset_index()[0]!=1)                   
        f_df=f_df.append(Bsel.iloc[:,:5])
    bmodglob=f_df.groupby('Modulo',as_index=False).agg({'FV':sum}).sort_values(by=['FV'], ascending=False)   
    bmod=bmodglob.head(1)
    f_df.sort_index(inplace=True)
    bline=f_df[f_df['Modulo']==int(bmod['Modulo'])]
    bline['Modulo']=[int(x) for x in bline['Modulo']]
    return bline
                    
def generate_table(data):
    return dash_table.DataTable(data=data.to_dict('records'),columns=[{"name": i, "id": i} for i in data.columns],sort_action='native', filter_action='native', style_cell={'font-family':'Calibri','text-align':'left'},
                                     style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}
    ],style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'})


def generate_lo_sq(squad,n,l):
    return [html.H1(squad, id='nome-'+n, title=squad, style={'textAlign': 'center', 'background-image':'url("/assets/'+str(l)+'logo.png")',
                                                             'background-position': 'left', 'background-repeat': 'no-repeat', 'background-size': '15% 85%',
                                                             'font-size': '350%'}),
            html.Div([
                dbc.Tabs([dbc.Tab(dbc.Container([
                        html.H3('Organigramma'), dbc.Row([ dbc.Col(
                        dbc.Card( [dbc.CardImg(src='assets/people/'+str(l)+'pres.jpg',top=True),
                    dbc.CardBody([  html.H4("Presidente",),
                                    html.H6( organigramma[(organigramma['Stagione']==max(organigramma['Stagione'])) & (organigramma['Squadra']==squad)]['Presidente'] ),
                                ])]), width=4),
                dbc.Col(dbc.Card( [dbc.CardImg(src='assets/people/'+str(l)+'ds.jpg',top=True),
                    dbc.CardBody([  html.H4("DS", className="card-title"),
                                    html.H6(organigramma[(organigramma['Stagione']==max(organigramma['Stagione'])) & (organigramma['Squadra']==squad)]['DS'])
                              ])]), width=4),
                dbc.Col(dbc.Card( [dbc.CardImg(src='assets/people/'+str(l)+'mr.jpg',top=True),
                    dbc.CardBody([  html.H4("Mister", className="card-title"),
                                    html.H6(organigramma[(organigramma['Stagione']==max(organigramma['Stagione'])) & (organigramma['Squadra']==squad)]['Allenatore'])
                              ])]), width=4) ])
                        ]),label='Società'),
                          
                        dbc.Tab(dbc.Container([
                            html.H1('Rosa Attuale'), html.Br(),
                            html.P(id='ngio-'+n), html.Br(),
                            html.Div(id='t1-'+n)
                        ]), label='Rosa'),

                          dbc.Tab(dbc.Container([
                              dcc.Dropdown(
                                  options=[{'label':i,'value':i} for i in sorted(set(mercato['Stagione']))],
                              placeholder='Seleziona una stagione', id='season-choice1-'+n),
                                     html.H3('I numeri'),
                                dcc.Graph(id='mp-'+n),
                            dbc.Row([
                                dbc.Col([html.H6('Stipendi maggiori'), html.Div(id='high-salary-'+n)],className='w-30'),
                                dbc.Col([html.H6('Giocatori più usati'), html.Div(id='stakanov-' + n)],className='w-30'),
                                dbc.Col([html.H6('Le rabbie'), html.Div(id='mannagg-'+n)],className='w-30')
                            ])]),      label='General stats', tab_id='gen-stat-sq'),

                          dbc.Tab(dbc.Container([
                              dcc.Dropdown(
                                  options=[{'label':i,'value':i} for i in sorted(set(mercato['Stagione']))],
                              placeholder='Seleziona una stagione', id='season-choice-'+n),
                            html.H3('Bilancio'),
                            dbc.Row([
                                dcc.Graph(id='spese-'+n),
                                dcc.Graph(id='entrate-' + n),
                                daq.LEDDisplay(id='profit-'+n,label="Profitto",backgroundColor='#0c23f2',size=70),
#                                daq.Gauge(id='profit-'+n,color={"gradient":True,"ranges":{"red":[0,4],"yellow":[4,6],"green":[6,10]}},
#                                      min=-100,max=100, label='Profitto',showCurrentValue=True,units="€")
                            ]),
                            html.H3('Movimenti di mercato'),
                            dbc.Row([ dbc.Col([
                                html.H6('Arrivi'),
                                html.Div(id='arrivi-' + n)
                            ], className='w-45'), dbc.Col([
                                html.H6('Partenze'),
                                html.Div(id='partenze-' + n)
                            ], className='w-45')
                                ])
                        ]), label='Bilancio-Trasf', tab_id='bil-tras')
                          ])
            ] ), html.Br(), dbc.Button('Home',href='/',color='Primary',size='lg')
            ]


FantaApp = dash.Dash(__name__,external_stylesheets=[dbc.themes.SANDSTONE], eager_loading=True)
server = FantaApp.server

url_bar = dbc.Container([dcc.Location(id='url', refresh=False),
                        html.Div(id='page-content')
                        ])

index_page = dbc.Container([ dbc.Jumbotron([
    html.H1('FantaTim Manager', style={'color':'purple','fontSize':110,'font-family':'Trebuchet MS'}),
    html.H3('Il fantacalcio come non lo avete mai visto',style={'fontSize':40,'font-family':'roboto','textAlign':'center','background-color':'white'}) 
#                                      'background-repeat': 'no-repeat',
#                                      'background-position': 'center',
#                                      'background-size': '100% 100%'
],fluid=True), html.Br(), html.Br(),
    dbc.Nav([dbc.NavItem(dbc.DropdownMenu([dbc.DropdownMenuItem('Agghiaggiande',href='/agghiaggiande'),
                                           dbc.DropdownMenuItem('Aquile Estensi',href='/aquile-estensi'),
                                           dbc.DropdownMenuItem('Cimamori la Verace', href='/cimamori-la-verace'),
                                           dbc.DropdownMenuItem('Diavoli Felsinei', href='/diavoli-felsinei'),
                                           dbc.DropdownMenuItem('Doria Emiliana', href='/doria-emiliana'),
                                           dbc.DropdownMenuItem('Los Angeles Showtime', href='/los-angeles-showtime'),
                                           dbc.DropdownMenuItem('Parter', href='/parter'),
                                           dbc.DropdownMenuItem('The Lumberjacks', href='/the-lumberjacks'),
                                           dbc.DropdownMenuItem('Vanndoria', href='/vanndoria'),
                                           dbc.DropdownMenuItem('Zena Viola', href='/zena-viola'),
                                           ], label='Le Squadre',nav=True)),
             dbc.NavItem(dbc.NavLink('Competizioni',href='/competizioni',active=True)),
             dbc.NavItem(dbc.NavLink('Giocatori',href='/players',active=True)),
             dbc.NavItem(dbc.NavLink('Top 11',href='/top11',active=True)),
             dbc.NavItem(dbc.NavLink('Albo d\'oro',href='/palmares',active=True))],pills=True),
                html.Br(),
             dbc.Row([
                dbc.Card( [dbc.CardImg(src='assets/cash.jpg',top=True),
                    dbc.CardBody([  html.H4("400 €", className="card-title"),
                                    html.H6("Montepremi", className="card-subtitle"),
                                html.P('+ bonus')])], className='w-25'),
                dbc.Card( [dbc.CardImg(src='assets/formazione.jpg',top=True),
                    dbc.CardBody([  html.H4("10", className="card-title"),
                                    html.H6("Squadre", className="card-subtitle")
                              ])], className='w-25'),
                dbc.Card( [dbc.CardImg(src='assets/competizione.jpg',top=True),
                    dbc.CardBody([  html.H4("5", className="card-title"),
                                    html.H6("Competizioni", className="card-subtitle")
                              ])], className='w-25'),
                dbc.Card( [dbc.CardImg(src='assets/ranking.jpg',top=True),
                    dbc.CardBody([  html.H4("Inf", className="card-title"),
                                    html.H6("Stagioni", className="card-subtitle")
                              ])], className='w-25')
             ])
])

aqes=dbc.Container(generate_lo_sq('Aquile Estensi','01','ae'))
aggh=dbc.Container(generate_lo_sq('Agghiaggiande','02','agg'))
cima=dbc.Container(generate_lo_sq('Cimamori la Verace','03','cim'))
dife=dbc.Container(generate_lo_sq('Diavoli Felsinei','04','df'))
doel=dbc.Container(generate_lo_sq('Doria Emiliana','05','dor'))
lash=dbc.Container(generate_lo_sq('Los Angeles Showtime','06','la'))
part=dbc.Container(generate_lo_sq('Parter','07','par'))
thel=dbc.Container(generate_lo_sq('The Lumberjacks','08','tl'))
vann=dbc.Container(generate_lo_sq('Vanndoria','09','van'))
zevi=dbc.Container(generate_lo_sq('Zena Viola','10','zv'))

pcomp = dbc.Container([html.H1('Competizioni'),
                     dcc.Dropdown(options=[{'label':i,'value':i} for i in sorted(set(campionato['Stagione']))],
                             placeholder='Seleziona una stagione', id='season-choice-camp'),
                    html.Br(),
                    html.Br(),
                dbc.Tabs([
                        dbc.Tab(dbc.Container([
                            html.H1('Classifica'),
                            html.Div(id='class-camp'), html.Br(),
                            html.H3('Punti vs Punti tot'),
                            dcc.Graph(id='reg-pl'), html.Br(),
                            daq.LEDDisplay(id='mntp-ch',label="Montepremi prossima Champions",backgroundColor='#0070ba',size=40),
                            daq.LEDDisplay(id='mntp-eu',label="Montepremi prossima EU League",backgroundColor='#deb647',size=40),
                            daq.LEDDisplay(id='mntp-bm',label="Montepremi prossima SuperCup",backgroundColor='#ba7300',size=40),
                             ]), label='Campionato'
                        ),
                        dbc.Tab(dbc.Container([ dbc.Row([ dbc.Col([
                            html.H4('Gruppo A'),
                            html.Div(id='gr-a')], className='w-45'),
                            dbc.Col([
                            html.H4('Gruppo B'),
                            html.Div(id='gr-b')], className='w-45') ]),
                            html.H2('Finale'), html.Br()
                                    
                        ]), label='Coppa'),
                        dbc.Tab(dbc.Container([
                                html.H4('Champions League'), html.Br(),
                                
                                html.H4('Europa League'),
                                html.H4('Birra Moretti')]),label='Europa')
        ]), html.Br(),
    dbc.Button('Home',href='/',color='Primary',size='lg')
    ])
    
pplay = dbc.Container([html.H1('Giocatori'),
                dcc.Dropdown(options=[{'label':i,'value':i} for i in sorted(set(giocatori['ID']))],
                placeholder='Seleziona un giocatore', id='play-choice'),
                html.Br(),
                html.H3('Prestazioni attuali'),
                dcc.Graph(id='act-seas-play'),
                html.H3('Carriera FantaTim'),
                html.Div(id='career'), html.Br(),
    dbc.Button('Home',href='/',color='Primary',size='lg')
        ])    

ptop = dbc.Container([ html.H1('Best 11'), html.Br(),
                dcc.Dropdown(options=[{'label':i,'value':i} for i in sorted(set(voti['Stagione']))],
                placeholder='Seleziona una stagione', id='s-b11-choice'), html.Br(),
                dcc.Slider(id='gio-b11',min=1,max=38,value=voti.iloc[voti.shape[0]-1,13],marks={i:str(i) for i in range(1,39)}), html.Br(),
                html.H3('Globale'),
                dcc.Graph(id='gr-line-b11'), daq.LEDDisplay(id='pnt-tot-b11',label="Punteggio massimo totale",backgroundColor='#0070ba',size=40), html.Br(),
                html.H3('Per squadra'), html.Br(),
                dcc.Dropdown(options=[{'label':i,'value':i} for i in sorted(set(organigramma['Squadra']))],
                placeholder='Seleziona una squadra', id='team-b11-choice'), html.Br(),                
                dbc.Row([ dbc.Col([ html.H6('Formazione migliore'), html.Div(id='tm-line-b11')],className='w-45'), dbc.Col([ html.H6('Formazione schierata'), html.Div(id='act-line')],className='w-45') ])
        ])

ppal = dbc.Container([html.H1('Albo d\'oro'), html.Br(), html.Br(),
                      html.H3('Campionato'),html.Br(),html.P('2019-20: annullato'),
                      html.H3('Coppa'),html.Br(),html.P('2019-20: annullato'),
                      html.H3('Champions League'),html.Br(),html.P('2020-21: Zena Viola'),
                      html.H3('Europa League'),html.Br(),html.P('2020-21: The Lumberjacks'),
                      html.H3('Birra Moretti'),html.Br(),html.P('2020-21: Cimamori la Verace')])
    
def serve_layout():
    if flask.has_request_context():
        return url_bar
    return dbc.Container([
        url_bar,
        index_page,
        aqes, aggh, cima, dife, doel, lash, part, thel, vann, zevi,
        pcomp, 
        pplay,
        ptop, ppal
    ])


FantaApp.layout = serve_layout

@FantaApp.callback(Output('page-content','children'),
              [Input('url','pathname')])
def display_page(pathname):
    if pathname == "/aquile-estensi":
        return aqes
    elif pathname == "/agghiaggiande":
        return aggh
    elif pathname == "/cimamori-la-verace":
        return cima
    elif pathname == "/diavoli-felsinei":
        return dife
    elif pathname == "/doria-emiliana":
        return doel
    elif pathname == "/los-angeles-showtime":
        return lash
    elif pathname == "/parter":
        return part
    elif pathname == "/the-lumberjacks":
        return thel
    elif pathname == "/vanndoria":
        return vann
    elif pathname == "/zena-viola":
        return zevi
    elif pathname == "/competizioni":
        return pcomp
    elif pathname == "/players":
        return pplay
    elif pathname == "/top11":
        return ptop
    # elif pathname == "/market":
    #     return p4
    elif pathname == "/palmares":
        return ppal
    else:
        return index_page

for i in ['01','02','03','04','05','06','07','08','09','10']:
    @FantaApp.callback([Output('t1-'+i,'children'),
                        Output('ngio-'+i,'children')],
                        [Input('nome-'+i,'title')])
    def act_ros(team):
        df=anag_players(team)
        df=df.drop('Nome',axis=1).drop('Squadra',axis=1)
        df=df[['Nome Completo', 'Ruolo', 'Data Nascita', 'Luogo Nascita', 'Nazionalità', 'Età',
                       'Tipo Contratto', 'Fine Prestazione', 'Value Act', 'Value Ini']]
        df['Delta stag'] = (df['Value Act']-df['Value Ini']).apply(lambda x: '😄️' if x > 0 else '☹️' if x < 0 else '😶')
        df['Value Act'] = ['€{:,.2f}'.format(x) for x in df['Value Act']]
        df['Value Ini'] = ['€{:,.2f}'.format(x) for x in df['Value Ini']]
        return [generate_table(df), 'Numero giocatori: '+str(df.shape[0])]

for i in ['01','02','03','04','05','06','07','08','09','10']:
    @FantaApp.callback([Output('profit-'+i,'value'),
                        Output('spese-'+i,'figure'),
                        Output('entrate-' + i, 'figure'),
                        Output('arrivi-' + i, 'children'),
                        Output('partenze-' + i, 'children')],
                        [Input('nome-'+i,'title'),
                         Input('season-choice-'+i,'value')])
    def prof_team(team, seas):
        df = mercato[mercato['Stagione'] == seas]
        arr = df[(df['A'] == team) & (df['Tipo_operazione'] != 'RIN') & (df['Tipo_operazione'] != 'SVI')]
        cess = df[df['Da'] == team]
        arr = arr[['Data', 'Nome', 'Da', 'Spesa A', 'Tipo_operazione', 'Costo contratto']]
        cess = cess[['Data', 'Nome', 'A', 'Entrata Da', 'Tipo_operazione']]
        arr.columns = ['Data', 'Nome', 'Venditore', 'Spesa', 'Tipo op', 'Contratto']
        cess.columns = ['Data', 'Nome', 'Acquirente', 'Entrata', 'Tipo op']
        
        va = voti_arrk()
        stip = va[(va['Stagione'] == seas) & (va['A'] == team)]['Stipendio'].sum()
        spese = df[df['A'] == team]
        spese['Tipo_operazione'] = ['PRE' if x.startswith('PRE') else x for x in spese['Tipo_operazione']]
        speset = spese.groupby(['Tipo_operazione'], as_index=False).agg({'Spesa A': 'sum'})
        speset.columns = ['Voce Costo', 'Spesa']
        cont = spese['Costo contratto'].sum()
        riep_sp = pd.concat([speset, pd.DataFrame({'Voce Costo': 'Stipendi', 'Spesa': [stip]}),
                             pd.DataFrame({'Voce Costo': 'Contratti', 'Spesa': [cont]}),
                             pd.DataFrame({'Voce Costo': 'Quota', 'Spesa': [40]})])

        entrate = cess
        entrate['Tipo op'] = ['PRE' if x.startswith('PRE') else x for x in cess['Tipo op']]
        entratet = entrate.groupby(['Tipo op'], as_index=False).agg({'Entrata': 'sum'})
        entratet.columns = ['Voce Entrata', 'Entrata']
        premi = organigramma[(organigramma['Squadra'] == team) & (organigramma['Stagione'] == seas)][['Premio Cam', 'Premio Cop', 'Premio Eu']].sum(axis=1).squeeze()
        riep_en = pd.concat([entratet, pd.DataFrame({'Voce Entrata': 'Premi', 'Entrata': [premi]})])

        profitto = riep_en['Entrata'].sum() - riep_sp['Spesa'].sum()

        arr['Spesa'] =arr['Spesa'].map('€{:,.2f}'.format)
        arr['Contratto'] = arr['Contratto'].map('€{:,.2f}'.format)
        cess['Entrata'] = cess['Entrata'].map('€{:,.2f}'.format)
        arr['Data'] = [x.date() for x in arr['Data']]
        cess['Data'] = [x.date() for x in cess['Data']]

        figsp = go.Figure(data=[go.Pie(labels=riep_sp['Voce Costo'], values=riep_sp['Spesa'], title='Spese')])
        figen = go.Figure(data=[go.Pie(labels=riep_en['Voce Entrata'], values=riep_en['Entrata'], title='Entrate')])
        return [round(profitto,2), figsp, figen, generate_table(arr), generate_table(cess)]

for i in ['01','02','03','04','05','06','07','08','09','10']:
    @FantaApp.callback([Output('mp-' + i, 'figure'),
                        Output('high-salary-'+i,'children'),
                        Output('stakanov-' + i, 'children'),
                        Output('mannagg-' + i, 'children')],
                        [Input('nome-'+i,'title'),
                         Input('season-choice1-'+i,'value')])
    def numeri_team(team, seas):
        va = voti_arrk()
        va = va[(va['A']==team) & (va['Stagione']==seas)]
        vagg = va.groupby(['Nome'],as_index=False).agg({'Stipendio':'sum'})
        vsort = vagg.sort_values(by=['Stipendio'],ascending=False).head(10)    
        vsort.loc[vsort.shape[0]]=['OVERALL:',vagg['Stipendio'].sum()]
        vsort['Stipendio'] = vsort['Stipendio'].map('€{:,.2f}'.format)

        vagg1 = va.groupby(['Nome'],as_index=False).agg({'Titolarita':'sum'})
        vsort1 = vagg1.sort_values(by=['Titolarita'],ascending=False).head(10)  
        
        varab = va[va['Titolarita']==0][['Nome','Giornata','FV']].sort_values(by=['FV'],ascending=False).head(10)
        
        ca = campionato[(campionato['Sq casa']==team) & (campionato['Stagione']==seas)][['Giornata','Pnt casa']]
        ca.columns=['G','Pnt']
        tr = campionato[(campionato['Sq tras']==team) & (campionato['Stagione']==seas)][['Giornata','Pnt tras']]
        tr.columns=['G','Pnt']
        pth = ca.append(tr).sort_values(by=['G'])
        linemp=go.Figure(data=go.Scatter(x=pth['G'],y=pth['Pnt']))
        linemp.add_trace(go.Scatter(x=pth['G'],y=[np.nanmean(pth['Pnt'])]*pth['G'].max(), mode='lines', line=dict(color='purple',dash='dashdot')))
        linemp.add_annotation(go.layout.Annotation(x=0.01,y=0.5,text='MP: '+str(round(np.nanmean(pth['Pnt']),2)),bgcolor='#ff7f0e',opacity=0.8,showarrow=False))
        linemp.update_layout(title='Andamento punti totali',xaxis_title='Giornata',yaxis_title='Punti')
        return [linemp, generate_table(vsort),generate_table(vsort1),generate_table(varab)]        


@FantaApp.callback([Output('mntp-ch', 'value'),
                    Output('mntp-eu','value'),
                    Output('mntp-bm', 'value'),
                    Output('class-camp', 'children'),
                    Output('gr-a','children'),
                    Output('gr-b', 'children'),
                    Output('reg-pl','figure')
                    ],
                    [Input('season-choice-camp','value')])
def cla(s):
    cc=classifica(campionato,s)
    v=voti_arrk()
    # v1=v[v['Stagione']==s]
    # ldif,squ=[],[]
    # for team in sorted(set(organigramma['Squadra'])):
    #     for gio in list(range(3,max(v1['Giornata'])+1)):
    #         ldif.append(float(b11(s,gio,team)['FV'].sum())-float(v1.loc[(v1['A']==team) & (v1['Giornata']==gio) & (v1['Titolarita']==1),'FV'].sum()))
    #         squ.append(team)
    # d1=pd.DataFrame({'Squadra':squ,'MPntLost':ldif})
    # dgr=d1.groupby(['Squadra'],as_index=False).agg({'MPntLost':'mean'})
    contro_c=contro_class(s)
    ms=v[(v['Stagione']==s) & (pd.notnull(v['A']))]['Stipendio'].sum()
    cc=pd.merge(cc, contro_c, on='Squadra', how='inner')
#    cc=pd.merge(cc, dgr, on='Squadra',how='left')
    if s=='2020-21':
        cc.loc[cc['Squadra']=='Agghiaggiande','Pnt']=cc.loc[cc['Squadra']=='Agghiaggiande','Pnt']-5
        cc=cc.sort_values(by=['Pnt','P Glob','GF'], ascending=False)
    cc['Gay Index'] = (cc['Exp Pnt']-cc['Pnt']).apply(lambda x: '🦾' if x > 0 else '👨‍❤️‍💋‍👨' if x < 0 else '🤔')
    cc['Premio']=[85+ms*.17, 65+ms*.135, 55+ms*.105, 40+ms*.0875, 35+ms*.0775, 30+ms*.07, 25+ms*.0625, 20+ms*.055, 15+ms*.0475, 10+ms*.04]
    cc['Premio']=cc['Premio'].map('€{:,.2f}'.format)
    pcl=round(ms*.07,2)
    peu=round(ms*.05,2)
    pbm=round(ms*.03,2)
    b,m=polyfit(cc['P Glob'],cc['Pnt'],1)
    lin=[x*m for x in cc['P Glob']]
    reg_plot=go.Figure([go.Scatter(x=cc['P Glob'],y=cc['Pnt'],hovertext=cc['Squadra'],mode='markers',marker=dict(size=cc['GF'])),
                        go.Scatter(x=cc['P Glob'],y=b+lin)])
    reg_plot.update_yaxes(title_text='Punti')
    reg_plot.update_xaxes(title_text='P Glob')
    #c=coppa[(coppa['Stagione']==s) & (coppa['Gruppo']=='Finale')]
    #img1='/assets/'+str(sigle[c['Sq casa'].squeeze()])+'shirt.png'    
    #img2='/assets/'+str(sigle[c['Sq tras'].squeeze()])+'shirt.png'    
    return[pcl,peu,pbm,generate_table(cc),generate_table(classifica(coppa,s,'A')),generate_table(classifica(coppa,s,'B')),
           reg_plot]
    
@FantaApp.callback([Output('act-seas-play', 'figure'),
                    Output('career','children')],
                    [Input('play-choice','value')])
def players(p):
    v=voti_arrk()
    df=v[(v['Nome']==p) & (v['Stagione']==max(v['Stagione']))].sort_values('Giornata')     
    grpl=go.Figure()
    grpl.add_trace(go.Scatter(x=df['Giornata'],y=df['Voto'],fill='tozeroy'))
    grpl.add_trace(go.Scatter(x=df['Giornata'],y=df['FV'],fill='tonexty'))
    grpl.add_trace(go.Scatter(x=df['Giornata'].unique().tolist(),y=[np.nanmean(df['Voto'])]*df['Giornata'].max(),mode='lines',line=dict(color='RoyalBlue',dash='dashdot')))
    grpl.add_trace(go.Scatter(x=df['Giornata'].unique().tolist(),y=[np.nanmean(df['FV'])]*df['Giornata'].max(),mode='lines',line=dict(color='red',dash='dash')))
    grpl.add_annotation(go.layout.Annotation(x=0.1,y=0.5,text='FV: '+str(round(np.nanmean(df['FV']),2)),bgcolor='#ff7f0e',opacity=0.8,showarrow=False))
    grpl.add_annotation(go.layout.Annotation(x=0.9,y=0.5,text='MV: '+str(round(np.nanmean(df['Voto']),2)),bgcolor='#64e6e8',opacity=0.8,showarrow=False))
    grpl.update_yaxes(title_text='Voto')
    grpl.update_xaxes(title_text='Giornata')
    df1=v[(v['Nome']==p) & (v['Giornata']>2)]
    carr=df1.groupby(['Stagione','A'],as_index=False).agg({'Titolarita':'sum','Gf':'sum','Rf':'sum','Ass':'sum','Gs':'sum','Rp':'sum','Rs':'sum','PI':'sum','Au':'sum','Amm':'sum','Esp':'sum','Stipendio':'sum','Voto':'mean','FV':'mean'})
    carr.columns=['Stagione','Squadra','Pres','Gol F','Gol R','Ass','Gol S','Rig P','Reti S','P Inv','Aut','Amm','Esp','Stip','MV','FV']
    carr['Stip']=carr['Stip'].map('€{:,.2f}'.format)
    carr['MV']=[round(x,2) for x in carr['MV']]
    carr['FV']=[round(x,2) for x in carr['FV']]
    
    return[grpl,generate_table(carr)]

@FantaApp.callback([Output('gr-line-b11', 'figure'),Output('pnt-tot-b11', 'value'),
                    Output('tm-line-b11','children'),
                    Output('act-line','children')],
                    [Input('s-b11-choice','value'),Input('gio-b11','value'),
                     Input('team-b11-choice','value')])
def gen_b11(s,g,t):
    dfg=b11(s,g,t='All')
    v=voti_arrk()
    v1=v[(v['Stagione']==s) & (v['Giornata']==g)]
    dfg_arr=pd.merge(dfg,v1[['Nome','Titolarita','A']],on='Nome',how='left')
    dfg_arr['x']=[pos_draw[str(int(dfg_arr.iloc[0,4]))][m][0][0] for m in dfg_arr['Pos']]
    dfg_arr['y']=[pos_draw[str(int(dfg_arr.iloc[0,4]))][m][0][1] for m in dfg_arr['Pos']]
    dfg_arr['col']=['orange' if t == 1 else 'grey' for t in dfg_arr['Titolarita']]
    fv=['Voto: '+str(x) for x in dfg_arr['FV']]
    team=['('+str(x)+')' for x in dfg_arr['A']]
    nome=dfg_arr['Nome'].tolist()
    data=go.Scatter(x=dfg_arr['x'],y=dfg_arr['y'],mode='markers+text',
                             showlegend=False,textposition='top center',text=nome,
                             marker=dict(color=dfg_arr['col'],size=10))
    layout = go.Layout(xaxis=dict(showgrid=False,ticks='',showticklabels=False),
                       yaxis=dict(autorange=True,showgrid=False,ticks='',showticklabels=False)
                       ,plot_bgcolor="lawngreen")
    fig=go.Figure(data=data,layout=layout)

    for i in list(range(len(fv))):
        fig.add_annotation(x=dfg_arr.iloc[i,7],y=dfg_arr.iloc[i,8],text=fv[i],xshift=10,showarrow=False)
        fig.add_annotation(x=dfg_arr.iloc[i,7],y=dfg_arr.iloc[i,8]+20,text=team[i],yshift=-18,showarrow=False)
    
    pnt_tot=dfg['FV'].sum()

    df_sq=b11(s,g,t=t)
    v2 = v[(v['Stagione'] == s) & (v['Giornata'] == g) & (v['A'] == t) & (v['Titolarita']==1)]
    l11_act = v2[['Nome','Ruolo','FV']]
    b11_tm = df_sq[['Nome','Ruolo','FV']]
    l11_act.reset_index(drop=True,inplace=True)
    b11_tm.reset_index(drop=True, inplace=True)
    l11_act.loc[l11_act.shape[0]]=['TOTALE','',l11_act['FV'].sum()]
    b11_tm.loc[b11_tm.shape[0]] = ['TOTALE', '', b11_tm['FV'].sum()]
    return [fig,pnt_tot,generate_table(b11_tm),generate_table(l11_act)]

if __name__ == "__main__":
    FantaApp.server.run()

