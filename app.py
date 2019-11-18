# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:33:35 2019

@author: user
"""
import flask
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table_experiments as dt
import dash_bootstrap_components as dbc

partite=pd.read_excel(r'C:\Users\user\Desktop\partite.xlsx')
formazioni=pd.read_excel(r'C:\Users\user\Desktop\formazioni.xlsx')
marcatori=pd.read_excel(r'C:\Users\user\Desktop\marcatori.xlsx')
eventi=pd.read_excel(r'C:\Users\user\Desktop\eventi.xlsx')

def classifica(anno,ngini=1,ngfin=42):
    sc,gc,vc,nc,pc,gfc,gsc=[],[],[],[],[],[],[]
    st,gt,vt,nt,pt,gft,gst=[],[],[],[],[],[],[]
    filty=partite[(partite['Stagione']==anno) & (partite['Giornata']>=ngini) & (partite['Giornata']<=ngfin)]
    l1=list(filty['Squadra casa'])+(list(filty['Squadra trasferta']))
    squad=list(set(l1))
    for i in squad:
        casa=filty[filty['Squadra casa']==i]
        vc.append(sum(casa['Gol casa']>casa['Gol tras']))
        nc.append(sum(casa['Gol casa']==casa['Gol tras']))
        pc.append(sum(casa['Gol casa']<casa['Gol tras']))
        gfc.append(sum(casa['Gol casa']))
        gsc.append(sum(casa['Gol tras']))
        gc.append(casa.shape[0])
        sc.append(i)
        
        tras=filty[filty['Squadra trasferta']==i]
        vt.append(sum(tras['Gol casa']<tras['Gol tras']))
        nt.append(sum(tras['Gol casa']==tras['Gol tras']))
        pt.append(sum(tras['Gol casa']>tras['Gol tras']))
        gft.append(sum(tras['Gol tras']))
        gst.append(sum(tras['Gol casa']))
        gt.append(tras.shape[0])
        st.append(i)
        
    if int(filty.iloc[0,11][:4])>1993:        
        pnc=[x+y for x,y in zip(nc,[3*x for x in vc])]
        pnt=[x+y for x,y in zip(nt,[3*x for x in vt])]
    else:
        pnc=[x+y for x,y in zip(nc,[2*x for x in vc])]
        pnt=[x+y for x,y in zip(nt,[2*x for x in vt])]
        
    cl_casa=pd.DataFrame({'Squadra':sc,'Punti':pnc,'G':gc,'W':vc,'D':nc,'L':pc,'GF':gfc,'GS':gsc})
    cl_trasferta=pd.DataFrame({'Squadra':st,'Punti':pnt,'G':gt,'W':vt,'D':nt,'L':pt,'GF':gft,'GS':gst})
    
    cl_casa=cl_casa.sort_values(by=['Punti'], ascending=False)
    cl_trasferta=cl_trasferta.sort_values(by=['Punti'], ascending=False)
    
    cla=pd.concat([cl_casa, cl_trasferta]).groupby(['Squadra'], as_index=False)[['Punti','G','W','D','L','GF','GS']].sum()  
    if (anno=='1947-1948') & (ngfin>=34):
        newp=cla[cla['Squadra']=='NAPOLI']['Punti']-34
        cla.at[cla[cla['Squadra']=='NAPOLI'].index.item(),'Punti']=newp
    if (anno=='1959-1960') & (ngfin>=34):
        newp=cla[cla['Squadra']=='GENOA']['Punti']-18
        cla.at[cla[cla['Squadra']=='GENOA'].index.item(),'Punti']=newp
    if (anno=='1973-1974') & (ngfin>=1):
        newp=cla[cla['Squadra']=='SAMPDORIA']['Punti']-3
        cla.at[cla[cla['Squadra']=='SAMPDORIA'].index.item(),'Punti']=newp
    if (anno=='1973-1974') & (ngfin>=30):
        newp1=cla[cla['Squadra']=='FOGGIA']['Punti']-6
        newp2=cla[cla['Squadra']=='VERONA']['Punti']-25
        cla.at[cla[cla['Squadra']=='FOGGIA'].index.item(),'Punti']=newp1
        cla.at[cla[cla['Squadra']=='VERONA'].index.item(),'Punti']=newp2
    if (anno=='1976-1977') & (ngfin>=30):
        newp=cla[cla['Squadra']=='NAPOLI']['Punti']-1
        cla.at[cla[cla['Squadra']=='NAPOLI'].index.item(),'Punti']=newp
    if (anno=='1979-1980') & (ngfin>=30):
        newp1=cla[cla['Squadra']=='MILAN']['Punti']-36
        newp2=cla[cla['Squadra']=='LAZIO']['Punti']-25
        cla.at[cla[cla['Squadra']=='MILAN'].index.item(),'Punti']=newp1
        cla.at[cla[cla['Squadra']=='LAZIO'].index.item(),'Punti']=newp2
    if (anno=='1980-1981') & (ngfin>=1):
        newp1=cla[cla['Squadra']=='BOLOGNA']['Punti']-5
        newp2=cla[cla['Squadra']=='AVELLINO']['Punti']-5
        newp3=cla[cla['Squadra']=='PERUGIA']['Punti']-5
        cla.at[cla[cla['Squadra']=='BOLOGNA'].index.item(),'Punti']=newp1
        cla.at[cla[cla['Squadra']=='AVELLINO'].index.item(),'Punti']=newp2  
        cla.at[cla[cla['Squadra']=='PERUGIA'].index.item(),'Punti']=newp3
    if (anno=='1986-1987') & (ngfin>=1):
        newp=cla[cla['Squadra']=='UDINESE']['Punti']-9
        cla.at[cla[cla['Squadra']=='UDINESE'].index.item(),'Punti']=newp
    if (anno=='1987-1988') & (ngfin>=1):
        newp=cla[cla['Squadra']=='EMPOLI']['Punti']-5
        cla.at[cla[cla['Squadra']=='EMPOLI'].index.item(),'Punti']=newp
    if (anno=='1998-1999') & (ngfin>=11):
        newp=cla[cla['Squadra']=='EMPOLI']['Punti']-2
        cla.at[cla[cla['Squadra']=='EMPOLI'].index.item(),'Punti']=newp
    if (anno=='2005-2006') & (ngfin>=38):
        newp1=cla[cla['Squadra']=='MILAN']['Punti']-30
        newp2=cla[cla['Squadra']=='LAZIO']['Punti']-30
        newp3=cla[cla['Squadra']=='FIORENTINA']['Punti']-30
        newp4=cla[cla['Squadra']=='JUVENTUS']['Punti']-91
        cla.at[cla[cla['Squadra']=='MILAN'].index.item(),'Punti']=newp1
        cla.at[cla[cla['Squadra']=='LAZIO'].index.item(),'Punti']=newp2  
        cla.at[cla[cla['Squadra']=='FIORENTINA'].index.item(),'Punti']=newp3
        cla.at[cla[cla['Squadra']=='JUVENTUS'].index.item(),'Punti']=newp4
    if (anno=='2006-2007') & (ngfin>=1) & (ngfin<9):
        newp1=cla[cla['Squadra']=='MILAN']['Punti']-8
        newp2=cla[cla['Squadra']=='LAZIO']['Punti']-11
        newp3=cla[cla['Squadra']=='FIORENTINA']['Punti']-19
        newp4=cla[cla['Squadra']=='REGGINA']['Punti']-15
        cla.at[cla[cla['Squadra']=='MILAN'].index.item(),'Punti']=newp1
        cla.at[cla[cla['Squadra']=='LAZIO'].index.item(),'Punti']=newp2  
        cla.at[cla[cla['Squadra']=='FIORENTINA'].index.item(),'Punti']=newp3
        cla.at[cla[cla['Squadra']=='REGGINA'].index.item(),'Punti']=newp4
    if (anno=='2006-2007') & (ngfin>=7):
        newp=cla[cla['Squadra']=='SIENA']['Punti']-1
        cla.at[cla[cla['Squadra']=='SIENA'].index.item(),'Punti']=newp
    if (anno=='2006-2007') & (ngfin>=9):
        newp1=cla[cla['Squadra']=='MILAN']['Punti']-8
        newp2=cla[cla['Squadra']=='LAZIO']['Punti']-3
        newp3=cla[cla['Squadra']=='FIORENTINA']['Punti']-15
        newp4=cla[cla['Squadra']=='REGGINA']['Punti']-11
        cla.at[cla[cla['Squadra']=='MILAN'].index.item(),'Punti']=newp1
        cla.at[cla[cla['Squadra']=='LAZIO'].index.item(),'Punti']=newp2  
        cla.at[cla[cla['Squadra']=='FIORENTINA'].index.item(),'Punti']=newp3
        cla.at[cla[cla['Squadra']=='REGGINA'].index.item(),'Punti']=newp4
    if (anno=='2010-2011') & (ngfin>=15) & (ngfin<20):
        newp=cla[cla['Squadra']=='BOLOGNA']['Punti']-1
        cla.at[cla[cla['Squadra']=='BOLOGNA'].index.item(),'Punti']=newp
    if (anno=='2010-2011') & (ngfin>=20):
        newp=cla[cla['Squadra']=='BOLOGNA']['Punti']-3
        cla.at[cla[cla['Squadra']=='BOLOGNA'].index.item(),'Punti']=newp
    if (anno=='2011-2012') & (ngfin>=1):
        newp=cla[cla['Squadra']=='ATALANTA']['Punti']-6
        cla.at[cla[cla['Squadra']=='ATALANTA'].index.item(),'Punti']=newp
    if (anno=='2012-2013') & (ngfin>=1):
        newp1=cla[cla['Squadra']=='SIENA']['Punti']-6
        newp2=cla[cla['Squadra']=='ATALANTA']['Punti']-2
        newp3=cla[cla['Squadra']=='TORINO']['Punti']-1
        newp4=cla[cla['Squadra']=='SAMPDORIA']['Punti']-1
        cla.at[cla[cla['Squadra']=='SIENA'].index.item(),'Punti']=newp1
        cla.at[cla[cla['Squadra']=='ATALANTA'].index.item(),'Punti']=newp2  
        cla.at[cla[cla['Squadra']=='TORINO'].index.item(),'Punti']=newp3
        cla.at[cla[cla['Squadra']=='SAMPDORIA'].index.item(),'Punti']=newp4
    if (anno=='2014-2015') & (ngfin>=15) & (ngfin<27):
        newp=cla[cla['Squadra']=='PARMA']['Punti']-1
        cla.at[cla[cla['Squadra']=='PARMA'].index.item(),'Punti']=newp
    if (anno=='2014-2015') & (ngfin>=27) & (ngfin<31):
        newp=cla[cla['Squadra']=='PARMA']['Punti']-3
        cla.at[cla[cla['Squadra']=='PARMA'].index.item(),'Punti']=newp
    if (anno=='2014-2015') & (ngfin>=31):
        newp=cla[cla['Squadra']=='PARMA']['Punti']-7
        cla.at[cla[cla['Squadra']=='PARMA'].index.item(),'Punti']=newp
    cla=cla.sort_values(by=['Punti'], ascending=False)
    cla.reset_index(drop=True,inplace=True)
    cl_casa.reset_index(drop=True,inplace=True)
    cl_trasferta.reset_index(drop=True,inplace=True)
    return [cl_casa, cl_trasferta, cla]

#app=Flask(__name__)
#
#@app.route("/")
#def home():
#    season=sorted(set(partite['Stagione']))
#    return render_template("home.html",season=season)
#
#@app.route("/<anno>")
#def cla(anno):
#    season=sorted(set(partite['Stagione']))
#    gio=set(partite[partite['Stagione']==anno]['Giornata'])
#    return render_template("home.html",tables=[classifica(anno,1,gio)[2].to_html(classes='data',header="true")],season=season,gio=gio)
#
#@app.route("/about")
#def about():
#    return render_template("about.html")
#
#if __name__ == "__main__":
#    app.run()


def generate_table(df):
    return dbc.Table( [html.Tr([html.Th(col) for col in df.columns])]+
                        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(df.shape[0])]
            ,bordered=True)

app=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
sea=sorted(set(partite['Stagione']))

url_bar=dbc.Container([dcc.Location(id='url',refresh=False),
                  html.Div(id='page-content')
        ])

index_page = dbc.Container(style={'background-image':'url("/assets/calcio.jpeg")',
                             'background-repeat': 'no-repeat',
                              'background-position': 'center',
                              'background-size':'100% 100%'
                              },
    children=[html.H1('FantaTim Manager 2k20',style={'color':'purple','fontSize':150,'font-family':'Trebuchet MS','textAlign':'center'}),
              html.H3('Il fantacalcio come non lo avete mai visto',style={'fontSize':50,'font-family':'roboto','textAlign':'center','background-color':'white'}),
    dbc.Nav([dbc.NavItem(dbc.NavLink('Go to Page 1', href='/class',active=True)),   
                dbc.NavItem(dbc.NavLink('Go to Page 2', href='/next',active=True))],pills=True)
])    
    
p1=dbc.Container([html.H1('Classifica e risultati'),
                    dcc.Dropdown(id='season', options=[{'label':i,'value':i} for i in sea], value='2019-2020'),
                    html.Hr(),
                    dcc.Slider(id='giornata',min=1 ),
                    html.Hr(),
                    html.Div([
                            html.Div(id='rank',className='six columns'),
                            html.Hr(),
                            html.Div(id='match',className='six columns')
                    ],className='row'),
                    html.Br(),
                    dcc.Link('Home',href='/'),
                    html.Br(),
                    dcc.Link('Prossima giornata',href='/next')
                    ])
    
p2=dbc.Container([html.H1('Prossima giornata')
                    , html.Br()
                    ,dcc.Link('Home',href='/')
                    ,html.Br()
                    ,dcc.Link('Classifica',href='/class')
                    ])

def serve_layout():
    if flask.has_request_context():
        return url_bar
    return dbc.Container([
        url_bar,
        index_page,
       p1,
        p2,
    ])  
    
app.layout=serve_layout
    
@app.callback(Output('page-content','children'),
              [Input('url','pathname')]) 
def display_page(pathname):
    if pathname == "/class":
        return p1
    elif pathname == "/next":
        return p2
    else:
        return index_page
    
@app.callback([Output('giornata','value'),
              Output('giornata','max'),
              Output('giornata','marks')],
              [Input('season','value')])
def set_gio_option(select_year):
    m=max(partite[partite['Stagione']==select_year]['Giornata'])
    return [max(partite[partite['Stagione']==select_year]['Giornata']),m,{i:str(i) for i in range(1,m+1)}]


@app.callback([Output('rank','children'),
               Output('match','children')],
              [Input('season','value'),
               Input('giornata','value')])        
def classf(s,g):
    partite['Day']=[x.date() for x in partite['Data']]
    partite['Risultato']=[str(x)+'-'+str(y) for x,y in zip(partite['Gol casa'],partite['Gol tras'])]
    return [generate_table(classifica(s,1,g)[2]), generate_table(partite[(partite['Giornata']==g) & (partite['Stagione']==s)][['Weekday','Day','Squadra casa','Squadra trasferta','Risultato']]) ]

 
if __name__ == "__main__":
    app.run_server()