# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 10:26:53 2021

@author: user
"""
import pandas as pd

import mysql.connector as sql_db
from sqlalchemy import create_engine

db_connection=create_engine("mysql+pymysql://root:"+'Marione33!'+"@localhost:3306/fanta")

ruolo=pd.read_excel(r'DBFanta.xlsx',sheet_name='Ruolo')
organigramma=pd.read_excel(r'DBFanta.xlsx',sheet_name='Organigramma')
giocatori=pd.read_excel(r'DBFanta.xlsx',sheet_name='Giocatori')
mercato=pd.read_excel(r'DBFanta.xlsx',sheet_name='Mercato')
campionato=pd.read_excel(r'DBFanta.xlsx',sheet_name='Campionato')
cup=pd.read_excel(r'DBFanta.xlsx',sheet_name='Cup')
moduli=pd.read_excel(r'Moduli.xlsx')
quotazioni=pd.read_excel(r'Quotazioni_new.xlsx')
voti=pd.read_excel(r'Voti_new.xlsx')

ruolo.to_sql(con=db_connection, name='ruolo',if_exists='replace',index=False)
organigramma.to_sql(con=db_connection, name='organigramma',if_exists='replace',index=False)
giocatori.to_sql(con=db_connection, name='giocatori',if_exists='replace',index=False)
mercato.to_sql(con=db_connection, name='mercato',if_exists='replace',index=False)
campionato.to_sql(con=db_connection, name='campionato',if_exists='replace',index=False)
cup.to_sql(con=db_connection, name='cup',if_exists='replace',index=False)
moduli.to_sql(con=db_connection, name='moduli',if_exists='replace',index=False)
quotazioni.to_sql(con=db_connection, name='quotazioni',if_exists='replace',index=False)
voti.to_sql(con=db_connection, name='voti',if_exists='replace',index=False)
