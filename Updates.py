# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:31:20 2020

@author: user
"""
import pandas as pd
import numpy as np
from datetime import date, timedelta
import os

voti=pd.read_excel(r'Voti_new.xlsx')
quotazioni=pd.read_excel(r'Quotazioni_new.xlsx')
gio=voti.iloc[voti.shape[0]-1,13]

if os.path.exists(r'C:\Users\user\Downloads\Voti_Fantacalcio_Stagione_2020-21_Giornata_'+str(gio+1)+'.xlsx') & os.path.exists(r'C:\Users\user\Downloads\Formazioni_fantatim-manager-2k20_'+str(gio-1)+'_giornata.xlsx'):
    f=pd.read_excel(r'C:\Users\user\Downloads\Formazioni_fantatim-manager-2k20_'+str(gio-1)+'_giornata.xlsx')
    f=f.iloc[4:,:]
    p=[1]
    
    for i in list(range(f.shape[0]-1)):
        if pd.isnull(f.iloc[i,0]) & pd.notnull(f.iloc[i+1,0]):
            p.append(p[len(p)-1]+1)
        else:
            p.append(p[len(p)-1])
    f['ID']=p
    f=f[pd.notnull(f.iloc[:,1])]
    l_tit=[]
    for i in list(range(1,6)):
        df=f[f.iloc[:,11]==i]
        for k in list(range(11)):
            if df.iloc[k,3]!='-':        
                l_tit.append(df.iloc[k,1].upper())
            if df.iloc[k,9]!='-':    
                l_tit.append(df.iloc[k,7].upper())
    Tit=pd.DataFrame({'Nome':l_tit,'Tit':[1]*len(l_tit)})
    voti_grez=pd.read_excel(r'C:\Users\user\Downloads\Voti_Fantacalcio_Stagione_2020-21_Giornata_'+str(gio+1)+'.xlsx')
    voti_grez_1=voti_grez.iloc[5:,1:]
    voti_grez_2=voti_grez_1[(voti_grez_1.iloc[:,0]!='ALL') & (voti_grez_1.iloc[:,0]!='Ruolo') & (pd.notnull(voti_grez_1.iloc[:,0]))]
    voti_grez_2.iloc[:,2]=[np.nan if '*' in str(x) else x for x in voti_grez_2.iloc[:,2]]
    vf_grezzi=voti_grez_2.iloc[:,1:13]
    vf_grezzi['Ass']=[x+y for x,y in zip(vf_grezzi.iloc[:,10],vf_grezzi.iloc[:,11])]
    vf_grezzi=vf_grezzi.iloc[:,[0,1,2,3,4,5,6,7,8,9,12]]
    vf_grezzi.columns=['Nome','Voto','Gf','Gs','Rp','Rs','Rf','Au','Amm','Esp','Ass']
    vf_grezzi['Titolarita']=[1 if x in l_tit else 0 for x in vf_grezzi['Nome']]
    if voti.iloc[voti.shape[0]-1,13]==38:
        vf_grezzi['Giornata']=[1]*vf_grezzi.shape[0]
    else:
        vf_grezzi['Giornata']=[voti.iloc[voti.shape[0]-1,13]+1]*vf_grezzi.shape[0]
    vf_grezzi['Stagione']=['2020-21']*vf_grezzi.shape[0]
    voti['Data']=[x.date() for x in voti['Data']]
    vf_grezzi['Data']=[date.today() - timedelta(days=1)]*vf_grezzi.shape[0]
    voti=voti.append(vf_grezzi)
    voti.to_excel(r'Voti_new.xlsx',index=False)

if os.path.exists(r'C:\Users\user\Downloads\Quotazioni_Fantacalcio_Ruoli_Mantra.xlsx'):
    q_grez=pd.read_excel(r'C:\Users\user\Downloads\Quotazioni_Fantacalcio_Ruoli_Mantra.xlsx')
    q_grez_1=q_grez.iloc[1:,2:5]
    q_grez_1.columns=['Nome','Squadra','Q']
    q_grez_1['Stagione']=['2020-21']*q_grez_1.shape[0]
    qf=pd.merge(quotazioni,q_grez_1,on=['Nome','Stagione'],how='left')
    qf['QA']=[y if pd.isnull(x) else x for x,y in zip(qf['Q'],qf['QA'])]
    qf['Diff']=[x-y for x,y in zip(qf['QA'],qf['QI'])]
    qf['VA']=[max(x+y*0.05,0.05) for x,y in zip(qf['VI'],qf['Diff'])]
    qf['VFA']=[round((x+y)/2,2) for x,y in zip(qf['VI'],qf['VA'])]
    qf=qf.drop('Squadra',axis=1).drop('Q',axis=1)    
    qf.to_excel(r'Quotazioni_new.xlsx',index=False)