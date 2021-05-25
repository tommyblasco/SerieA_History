from webfanta_function import *
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
import dash_daq as daq
import plotly.graph_objects as go
from plotly.offline import plot
import flask
import pandas as pd
import pandasql as ps
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
from datetime import date

webfanta = dash.Dash(__name__,external_stylesheets=[dbc.themes.FLATLY], eager_loading=True)
server = webfanta.server

url_bar = dbc.Container([dcc.Location(id='url', refresh=False),
                        html.Div(id='page-content')
                        ])

index_page = dbc.Container([ dbc.Jumbotron([
    html.H1('FantaTim Manager', style={'color':'purple','fontSize':110,'font-family':'Trebuchet MS'}),
    html.H3('Il fantacalcio come non lo avete mai visto',style={'fontSize':40,'font-family':'roboto','textAlign':'center','background-color':'white'})
#                                      'background-repeat': 'no-repeat',
#                                      'background-position': 'center',
#                                      'background-size': '100% 100%'
                            ],fluid=True, style={'background-image':'url("/assets/calcio.jpeg")','background-size':'cover'}), html.Br(), html.Br(),
    dbc.CardHeader( dbc.Button('Le Squadre', id='button-1',color='primary')),
    dbc.Collapse([
        dbc.Row([
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Agghiaggiande - logo.png",top=True), dbc.CardBody(dbc.CardLink('Agghiaggiande',href='/agghiaggiande'))]),width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Aquile Estensi - logo.png",top=True), dbc.CardBody(dbc.CardLink('Aquile Estensi',href='/aquile-estensi'))]),width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Cimamori la Verace - logo.png", top=True), dbc.CardBody(dbc.CardLink('Cimamori Maradona FC', href='/cimamori-maradona'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Diavoli Felsinei - logo.png", top=True), dbc.CardBody(dbc.CardLink('Diavoli Felsinei', href='/diavoli-felsinei'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Doria Emiliana - logo.png", top=True), dbc.CardBody(dbc.CardLink('AS Doria Emiliana', href='/doria-emiliana'))]), width=2)
        ],className='mb-2'),
        dbc.Row([
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Los Angeles Showtime - logo.png", top=True), dbc.CardBody(dbc.CardLink('Los Angeles Showtime', href='/los-angeles-showtime'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Parter - logo.png", top=True), dbc.CardBody(dbc.CardLink('Parter', href='/parter'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/The Lumberjacks - logo.jpeg", top=True), dbc.CardBody(dbc.CardLink('Der Holzfaller', href='/der-holzfaller'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Vanndoria - logo.png", top=True), dbc.CardBody(dbc.CardLink('Vanndoria', href='/vanndoria'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Zena Viola - logo.png", top=True), dbc.CardBody(dbc.CardLink('Zena Viola', href='/zena-viola'))]), width=2)
        ],className='mb-2')],id='collapse-1'),
    dbc.CardHeader( dbc.Button('Le Competizioni', id='button-2',color='primary')),
    dbc.Collapse(
        dbc.Row([
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Campionato.png", top=True), dbc.CardBody(dbc.CardLink('Campionato', href='/campionato'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Coppa Italia.png", top=True), dbc.CardBody(dbc.CardLink('Coppa', href='/cup'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Champions League.jpg", top=True), dbc.CardBody(dbc.CardLink('Champions League', href='/champions-league'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Europa League.png", top=True), dbc.CardBody(dbc.CardLink('Europa League', href='/europa-league'))]), width=2),
        dbc.Col(dbc.Card([dbc.CardImg(src="/assets/Supercup.jpg", top=True), dbc.CardBody(dbc.CardLink('Supercoppa Europea', href='/supercup'))]), width=2)
        ], className='mb-2'),id='collapse-2')
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

@webfanta.callback(Output('collapse-1','is_open'),[Input('button-1','n_clicks')],[State('collapse-1','is_open')])
def toggle_collapse(n,is_open):
    if n:
        return not is_open
    return is_open

@webfanta.callback(Output('collapse-2','is_open'),[Input('button-2','n_clicks')],[State('collapse-2','is_open')])
def toggle_collapse(n,is_open):
    if n:
        return not is_open
    return is_open

for i in ['01','02','03','04','05','06','07','08','09','10']:
    @webfanta.callback([Output('t1-'+i,'children'),
                        Output('ngio-'+i,'children')],
                        [Input('nome-'+i,'title')])
    def act_ros(team):
        df=rosa_act(team)
        df=df.drop('Nome',axis=1).drop('Squadra',axis=1)
        df=df[['Nome Completo', 'Ruolo', 'Data Nascita', 'Luogo Nascita', 'Nazionalità', 'Età',
                       'Tipo Contratto', 'Fine Prestazione', 'Value Act', 'Value Ini']]
        df['Delta stag'] = (df['Value Act']-df['Value Ini']).apply(lambda x: '😄️' if x > 0 else '☹️' if x < 0 else '😶')
        df['Value Act'] = ['€{:,.2f}'.format(x) for x in df['Value Act']]
        df['Value Ini'] = ['€{:,.2f}'.format(x) for x in df['Value Ini']]
        return [generate_table(df), 'Numero giocatori: '+str(df.shape[0])]

def serve_layout():
    if flask.has_request_context():
        return url_bar
    return dbc.Container([
        url_bar,
        index_page,
        aqes, aggh, cima, dife, doel, lash, part, thel, vann, zevi,
#        pcomp,
#        pplay,
#        ptop, ppal
    ])

webfanta.layout = serve_layout

@webfanta.callback(Output('page-content','children'),
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
#    elif pathname == "/competizioni":
#        return pcomp
#    elif pathname == "/players":
#        return pplay
#    elif pathname == "/top11":
#        return ptop
    # elif pathname == "/market":
    #     return p4
#    elif pathname == "/palmares":
#        return ppal
    else:
        return index_page

if __name__ == "__main__":
    webfanta.server.run()