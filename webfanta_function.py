import dash_table
import pandas as pd
import pandasql as ps
from datetime import date
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from sqlalchemy import create_engine

db_connection=create_engine("mysql+pymysql://b2a7bda2a76542:"+'6344bced'+"@us-cdbr-east-03.cleardb.com:3306/heroku_dedad33d323a4b8")

voti = pd.read_excel('Voti_new.xlsx')
mercato=pd.DataFrame(db_connection.execute('SELECT * FROM mercato'))
mercato.columns=db_connection.execute('SELECT * FROM mercato').keys()
ruolo=pd.DataFrame(db_connection.execute('SELECT * FROM ruolo'))
ruolo.columns=db_connection.execute('SELECT * FROM ruolo').keys()
giocatori=pd.DataFrame(db_connection.execute('SELECT * FROM giocatori'))
giocatori.columns=db_connection.execute('SELECT * FROM giocatori').keys()
quotazioni=pd.DataFrame(db_connection.execute('SELECT * FROM quotazioni'))
quotazioni.columns=db_connection.execute('SELECT * FROM quotazioni').keys()
organigramma = pd.read_excel('DBFanta.xlsx', sheet_name='Organigramma')
campionato = pd.read_excel('DBFanta.xlsx', sheet_name='Campionato')
coppa = pd.read_excel('DBFanta.xlsx', sheet_name='Cup')
moduli= pd.read_excel('Moduli.xlsx', sheet_name='Schema')



def rosa_act(team):
    fm = mercato[(mercato['Data'] <= pd.Timestamp('today').floor('D')) & (mercato['TP'] >= pd.Timestamp('today').floor('D')) & (mercato['A']==team)]
    r = ruolo[ruolo['Stagione']==max(ruolo['Stagione'])]
    q = quotazioni[quotazioni['Stagione']==max(quotazioni['Stagione'])]
    giocatori['Data_nascita'] = [x.date() for x in giocatori['Data_nascita']]
    today = date.today()
    giocatori['Age'] = [today.year - x.year - ((today.month, today.day) < (x.month, x.day)) for x in giocatori['Data_nascita']]
    ana1 = pd.merge(giocatori, fm[['A', 'Tipo_operazione', 'TP', 'Nome']], left_on='ID', right_on='Nome',
                    how='inner').drop('Nome_y',axis=1)
    ana2 = pd.merge(ana1, r[['Ruolo', 'Nome']], left_on='ID', right_on='Nome', how='left').drop('Nome',axis=1)
    ana_gio = pd.merge(ana2, q[['VA', 'Nome', 'VI']], left_on='ID', right_on='Nome', how='left').drop('Nome', axis=1)
    ana_gio.columns = ['Nome', 'Nome Completo', 'Data Nascita', 'Luogo Nascita', 'Nazionalità', 'Età', 'Squadra',
                       'Tipo Contratto', 'Fine Prestazione', 'Ruolo', 'Value Act', 'Value Ini']
    ana_gio['Fine Prestazione']=[x.date() for x in ana_gio['Fine Prestazione']]
    return ana_gio

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

def contro_class(s):
    df = campionato[campionato['Stagione'] == s]
    df_casa = df[['Giornata', 'Sq casa', 'Gol casa']]
    df_casa.columns = ['Giornata', 'Squadra', 'Gol']
    df_tras = df[['Giornata', 'Sq tras', 'Gol tras']]
    df_tras.columns = ['Giornata', 'Squadra', 'Gol']
    df = df_casa.append(df_tras).sort_values('Giornata')
    exp_p = []
    for k in list(set(df['Giornata'])):
        dfc = df[df['Giornata'] == k]
        dfc.reset_index(drop=True, inplace=True)
        for i in list(range(dfc.shape[0])):
            val_rif = dfc.iloc[i, 2]
            dfd = dfc.drop(i)
            exp_p.append(3 * sum(dfd['Gol'] < val_rif) / 9 + sum(dfd['Gol'] == val_rif) / 9)
    df.reset_index(drop=True, inplace=True)
    df_arr = pd.concat([df, pd.DataFrame({'Exp Pnt': exp_p})], axis=1)
    dagg = df_arr.groupby('Squadra', as_index=False).agg({'Exp Pnt': 'sum'})
    dagg['Exp Pnt'] = [int(x) for x in dagg['Exp Pnt']]
    return dagg

def b11(s, g, t='All'):
    v = voti_arrk()
    if t == 'All':
        v = v[(v['Giornata'] == g) & (v['Stagione'] == s)][['Nome', 'Ruolo', 'FV']]
    else:
        v = v[(v['Giornata'] == g) & (v['Stagione'] == s) & (v['A'] == t)][['Nome', 'Ruolo', 'FV']]
    lg_sort = v.sort_values('FV', ascending=False)
    lg_sort = lg_sort[pd.notnull(lg_sort['FV'])]
    lg_sort.reset_index(drop=True, inplace=True)
    f_df = pd.DataFrame()
    for modul in list(set(moduli['Modulo'])):
        modulis = moduli[moduli['Modulo'] == modul]
        df = pd.merge(lg_sort, modulis, on='Ruolo', how='left')
        df['Pos'] = df.iloc[:, 4:].apply(lambda x: x.index[x.astype(bool)].tolist(), 1)
        p, n, lun = [], [], []
        for i in list(range(df.shape[0])):
            for l in df.iloc[i, 15]:
                p.append(l)
                n.append(df.iloc[i, 0])
                lun.append(len(df.iloc[i, 15]))
        riep = pd.DataFrame({'Pos': p, 'N': n, 'Len': lun})
        f2 = pd.merge(riep, df.iloc[:, :4], left_on='N', right_on='Nome', how='left')
        f2 = f2.drop('N', axis=1).drop('Len', axis=1).sort_values('FV', ascending=False)
        Bsel = pd.merge(f2, f2.groupby('Pos', as_index=False).agg({'FV': 'max', 'Nome': 'first'}),
                        on=['Pos', 'FV', 'Nome'], how='right')
        Bsel['ID'] = [x + y for x, y in zip(Bsel['Pos'], Bsel['Nome'])]
        f2['ID'] = [x + y for x, y in zip(f2['Pos'], f2['Nome'])]
        sub = f2[~f2['ID'].isin(Bsel['ID'])]
        while Bsel.shape[0] < 11:
            Bsel.loc[Bsel.shape[0]] = ['', '', '', 0, Bsel.iloc[0, 4], '']
        count_dup = sum(pd.value_counts(list(filter(None, Bsel['Nome']))).to_frame().reset_index()[0] != 1)
        while count_dup != 0:
            for nn in list(filter(None, list(set(Bsel['Nome'])))):
                h = Bsel[Bsel['Nome'] == nn].shape[0]
                while h > 1:
                    selec = sub[sub['Pos'].isin(Bsel.loc[Bsel['Nome'] == nn, 'Pos'])].head(1)
                    if selec.shape[0] > 0:
                        Bsel[Bsel['Pos'] == selec.iloc[0, 0]] = selec.iloc[0, 0], selec.iloc[0, 1], selec.iloc[0, 2], \
                                                                selec.iloc[0, 3], selec.iloc[0, 4], selec.iloc[0, 5]
                    else:
                        Bsel = Bsel[~Bsel['Pos'].isin(Bsel.loc[Bsel['Nome'] == nn, 'Pos'].head(1))]
                        Bsel.reset_index(drop=True, inplace=True)
                        Bsel.loc[Bsel.shape[0]] = ['', '', '', 0, Bsel.iloc[0, 4], '']
                    sub = sub[~sub['ID'].isin(selec['ID'])]
                    h = h - 1
            count_dup = sum(pd.value_counts(list(filter(None, Bsel['Nome']))).to_frame().reset_index()[0] != 1)
        f_df = f_df.append(Bsel.iloc[:, :5])
    bmodglob = f_df.groupby('Modulo', as_index=False).agg({'FV': sum}).sort_values(by=['FV'], ascending=False)
    bmod = bmodglob.head(1)
    f_df.sort_index(inplace=True)
    bline = f_df[f_df['Modulo'] == int(bmod['Modulo'])]
    bline['Modulo'] = [int(x) for x in bline['Modulo']]
    return bline

def generate_table(data):
    return dash_table.DataTable(data=data.to_dict('records'),columns=[{"name": i, "id": i} for i in data.columns],sort_action='native', filter_action='native', style_cell={'font-family':'Calibri','text-align':'left'},
                                     style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}
    ],style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'})


def generate_lo_sq(squad, n, l):
    return [html.H1(squad, id='nome-' + n, title=squad,
                    style={'textAlign': 'center', 'background-image': 'url("/assets/' + str(l) + 'logo.png")',
                           'background-position': 'left', 'background-repeat': 'no-repeat',
                           'background-size': '15% 85%',
                           'font-size': '350%'}),
            html.Div([
                dbc.Tabs([dbc.Tab(dbc.Container([
                    html.H3('Organigramma'), dbc.Row([dbc.Col(
                        dbc.Card([dbc.CardImg(src='assets/people/' + str(l) + 'pres.jpg', top=True),
                                  dbc.CardBody([html.H4("Presidente", ),
                                                html.H6(organigramma[(organigramma['Stagione'] == max(
                                                    organigramma['Stagione'])) & (organigramma['Squadra'] == squad)][
                                                            'Presidente']),
                                                ])]), width=4),
                        dbc.Col(dbc.Card([dbc.CardImg(src='assets/people/' + str(l) + 'ds.jpg', top=True),
                                          dbc.CardBody([html.H4("DS", className="card-title"),
                                                        html.H6(organigramma[(organigramma['Stagione'] == max(
                                                            organigramma['Stagione'])) & (organigramma[
                                                                                              'Squadra'] == squad)][
                                                                    'DS'])
                                                        ])]), width=4),
                        dbc.Col(dbc.Card([dbc.CardImg(src='assets/people/' + str(l) + 'mr.jpg', top=True),
                                          dbc.CardBody([html.H4("Mister", className="card-title"),
                                                        html.H6(organigramma[(organigramma['Stagione'] == max(
                                                            organigramma['Stagione'])) & (organigramma[
                                                                                              'Squadra'] == squad)][
                                                                    'Allenatore'])
                                                        ])]), width=4)])
                ]), label='Società'),

                    dbc.Tab(dbc.Container([
                        html.H1('Rosa Attuale'), html.Br(),
                        html.P(id='ngio-' + n), html.Br(),
                        html.Div(id='t1-' + n)
                    ]), label='Rosa'),

                    dbc.Tab(dbc.Container([
                        dcc.Dropdown(
                            options=[{'label': i, 'value': i} for i in sorted(set(mercato['Stagione']))],
                            placeholder='Seleziona una stagione', id='season-choice1-' + n),
                        html.H3('I numeri'),
                        dcc.Graph(id='mp-' + n),
                        dbc.Row([
                            dbc.Col([html.H6('Stipendi maggiori'), html.Div(id='high-salary-' + n)], className='w-30'),
                            dbc.Col([html.H6('Giocatori più usati'), html.Div(id='stakanov-' + n)], className='w-30'),
                            dbc.Col([html.H6('Le rabbie'), html.Div(id='mannagg-' + n)], className='w-30')
                        ])]), label='General stats', tab_id='gen-stat-sq'),

                    dbc.Tab(dbc.Container([
                        dcc.Dropdown(
                            options=[{'label': i, 'value': i} for i in sorted(set(mercato['Stagione']))],
                            placeholder='Seleziona una stagione', id='season-choice-' + n),
                        html.H3('Bilancio'),
                        dbc.Row([
                            dcc.Graph(id='spese-' + n),
                            dcc.Graph(id='entrate-' + n),
                            daq.LEDDisplay(id='profit-' + n, label="Profitto", backgroundColor='#0c23f2', size=70),
                            #                                daq.Gauge(id='profit-'+n,color={"gradient":True,"ranges":{"red":[0,4],"yellow":[4,6],"green":[6,10]}},
                            #                                      min=-100,max=100, label='Profitto',showCurrentValue=True,units="€")
                        ]),
                        html.H3('Movimenti di mercato'),
                        dbc.Row([dbc.Col([
                            html.H6('Arrivi'),
                            html.Div(id='arrivi-' + n)
                        ], className='w-45'), dbc.Col([
                            html.H6('Partenze'),
                            html.Div(id='partenze-' + n)
                        ], className='w-45')
                        ])
                    ]), label='Bilancio-Trasf', tab_id='bil-tras')
                ])
            ]), html.Br(), dbc.Button('Home', href='/', color='Primary', size='lg')
            ]