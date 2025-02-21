import pandas as pd
import streamlit as st
st.set_page_config(page_title="Serie A - Squadre",layout='wide')
from Funzioni import *


tea_sel=st.selectbox('Seleziona una squadra',lista_sq)

df_casa=storico[storico['CASA']==tea_sel]
df_tras=storico[storico['TRAS']==tea_sel]

titcol1, titcol2 = st.columns([2, 1])
with titcol1:
    st.header(tea_sel)
with titcol2:
    st.image(Image.open(BytesIO(requests.get(load_images(team=tea_sel,yyyy='2999')).content)))

ov, inst, rec = st.tabs(['Overview','Insights','Record'])

with ov:
    st.subheader('Partecipazioni e pos finale:')
    st.markdown("*Qual è stata la posizione finale della squadra nelle varie stagioni in Serie A a cui ha partecipato?*")
    parcol1, parcol2 = st.columns([1, 3])
    with parcol1:
        n_part = int(riep_grp.loc[riep_grp['Squadre']==tea_sel,'Stagioni'].item())
        last_sea = riep_part.groupby('Squadre', as_index=False).agg({'Stagioni': 'max'})
        first_sea = riep_part.groupby('Squadre', as_index=False).agg({'Stagioni': 'min'})
        last_part = last_sea.loc[last_sea['Squadre'] == tea_sel, 'Stagioni'].item()
        first_part = first_sea.loc[first_sea['Squadre'] == tea_sel, 'Stagioni'].item()
        st.metric(label='N. Partecipazioni',value=n_part)
        st.metric(label='Esordio',value=first_part)
        st.metric(label='Ultima stagione',value=last_part)

    with parcol2:
        stag, pos = [], []
        for s in seas_list:
            cl = ranking(seas=s)
            if tea_sel in list(cl['Squadra']):
                pos.append(int(cl.loc[cl['Squadra']==tea_sel,'Rk'].item()))
            else:
                pos.append(np.nan)
            stag.append(s)
        df_pos = pd.DataFrame({'Stagione':seas_list}).merge(pd.DataFrame({'Stagione':stag,'Rank':pos}), on='Stagione', how='left')
        pos_gr = px.line(df_pos, x="Stagione", y="Rank", markers=True)
        pos_gr.update_layout(xaxis={'title':'Stagione','type':'category','autorange':'reversed'}, yaxis={'title':'Posizione','range':[21,0]})
        st.plotly_chart(pos_gr)

    st.divider()

    st.subheader('Bilancio serie A')
    st.markdown("*Clicca su un bottone sotto e scopri quante partite la squadra ha vinto, pareggiato o perso in Serie A e quanti gol ha realizzato o subito*")
    met_casa = [df_casa.shape[0], df_casa[df_casa['GC']>df_casa['GT']].shape[0], df_casa[df_casa['GC']==df_casa['GT']].shape[0],
                df_casa[df_casa['GC']<df_casa['GT']].shape[0], sum(df_casa['GC']), sum(df_casa['GT'])]
    met_tras = [df_tras.shape[0], df_tras[df_tras['GC']<df_tras['GT']].shape[0], df_tras[df_tras['GC']==df_tras['GT']].shape[0],
                df_tras[df_tras['GC']>df_tras['GT']].shape[0], sum(df_tras['GT']), sum(df_tras['GC'])]
    but_tot, but_h, but_a = st.columns(3)
    subc1, subc2, subc3, subc4 = st.columns(4)
    ssc1, ssc2 = st.columns(2)
    if but_tot.button('Totale',key='tot1'):
        subc1.metric(label='Giocate', value=met_casa[0]+met_tras[0])
        subc2.metric(label='Vinte', value=met_casa[1] + met_tras[1])
        subc3.metric(label='Pareggiate', value=met_casa[2] + met_tras[2])
        subc4.metric(label='Perse', value=met_casa[3] + met_tras[3])
        with ssc1:
            st.metric(label='Bilancio', value=met_casa[1] + met_tras[1] - met_casa[3] - met_tras[3], border=True)
            tot_bil_pie = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[met_casa[1]+met_tras[1], met_casa[2]+met_tras[2], met_casa[3]+met_tras[3]],
                           labels=["W", "D","L"])
            st.plotly_chart(go.FigureWidget(data=tot_bil_pie), use_container_width=True)
        with ssc2:
            st.metric(label='Diff Reti', value=met_casa[4] + met_tras[4] - met_casa[5] - met_tras[5], border=True)
            tot_g_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                                values=[met_tras[4]+met_casa[4], met_tras[5]+met_casa[5]],
                                labels=["GF", "GS"])
            st.plotly_chart(go.FigureWidget(data=tot_g_pie), use_container_width=True)
    if but_h.button('Casa',icon='🏚️',key='h1'):
        subc1.metric(label='Giocate',value=met_casa[0])
        subc2.metric(label='Vinte', value=met_casa[1])
        subc3.metric(label='Pareggiate', value=met_casa[2])
        subc4.metric(label='Perse', value=met_casa[3])
        with ssc1:
            st.metric(label='Bilancio', value=met_casa[1] - met_casa[3], border=True)
            home_bil_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                                 values=[met_casa[1], met_casa[2], met_casa[3]],
                                 labels=["W", "D", "L"])
            st.plotly_chart(go.FigureWidget(data=home_bil_pie), use_container_width=True)
        with ssc2:
            st.metric(label='Diff Reti', value=met_casa[4] - met_casa[5], border=True)
            home_g_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                                  values=[met_casa[4], met_casa[5]],
                                  labels=["GF", "GS"])
            st.plotly_chart(go.FigureWidget(data=home_g_pie), use_container_width=True)
    if but_a.button('Trasferta',icon='✈️',key='a1'):
        subc1.metric(label='Giocate',value=met_tras[0])
        subc2.metric(label='Vinte', value=met_tras[1])
        subc3.metric(label='Pareggiate', value=met_tras[2])
        subc4.metric(label='Perse', value=met_tras[3])
        with ssc1:
            st.metric(label='Bilancio', value=met_tras[1] - met_tras[3], border=True)
            away_bil_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                                 values=[met_tras[1],met_tras[2],met_tras[3]],
                                 labels=["W", "D", "L"])
            st.plotly_chart(go.FigureWidget(data=away_bil_pie), use_container_width=True)
        with ssc2:
            st.metric(label='Diff Reti', value=met_tras[4] - met_tras[5], border=True)
            away_g_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                                values=[met_tras[4], met_tras[5]],
                                labels=["GF", "GS"])
            st.plotly_chart(go.FigureWidget(data=away_g_pie), use_container_width=True)

with inst:
    df_casa_filt=df_casa[['Stagione','GC','GT']].rename(columns={'GC':'GF','GT':'GS'})
    df_tras_filt=df_tras[['Stagione','GT','GC']].rename(columns={'GT':'GF','GC':'GS'})
    df_casa_filt['C/T']=['C']*df_casa_filt.shape[0]
    df_tras_filt['C/T'] = ['T'] * df_tras_filt.shape[0]
    df_filt = pd.concat([df_casa_filt,df_tras_filt],ignore_index=True)
    df_filt['Pnt_real']=[3 if (x>y) & (z>='1994-95') else 2 if (x>y) & (z<'1994-95') else 1 if x==y else 0 for x,y,z in zip(df_filt['GF'],df_filt['GS'],df_filt['Stagione'])]
    df_filt['Pnt_hyp']=[3 if (x>y) & (z<'1994-95') else 1 if (x==y) & (z<'1994-95') else 0 if z<'1994-95' else np.nan for x,y,z in zip(df_filt['GF'],df_filt['GS'],df_filt['Stagione'])]
    st.markdown("*Clicca su un bottone sotto e scopri l'andamento stagionale della squadra per media punti (anche considerando sempre 3 pnt a vittoria) e media gol*")

    but_tot2, but_h2, but_a2 = st.columns(3)

    if but_tot2.button("Totale",key='tot2'):
        st.text('Media punti stagionale reale vs 3 pnt all time')
        avg_pnt=df_filt.groupby('Stagione',as_index=False).agg({'Pnt_real':'mean','Pnt_hyp':'mean'})
        avg_pnt_gr=go.Figure()
        avg_pnt_gr.add_trace(go.Scatter(x=avg_pnt['Stagione'],y=avg_pnt['Pnt_real'],line={'color':'orange'},mode='lines+markers',name='Pnt real'))
        avg_pnt_gr.add_trace(go.Scatter(x=avg_pnt['Stagione'],y=avg_pnt['Pnt_hyp'],line={'color':'blue','dash':'dash'},name='Pnt hyp'))
        avg_pnt_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Punti'})
        st.plotly_chart(go.FigureWidget(data=avg_pnt_gr), use_container_width=True)
        st.divider()
        st.text('Media gol fatti/subiti stagionale')
        avg_gol = df_filt.groupby('Stagione',as_index=False).agg({'GF':'mean','GS':'mean'})
        avg_gol_gr = go.Figure()
        avg_gol_gr.add_trace(go.Scatter(x=avg_gol['Stagione'],y=avg_gol['GF'],line={'color':'orange'},mode='lines+markers',name='GF'))
        avg_gol_gr.add_trace(go.Scatter(x=avg_gol['Stagione'],y=avg_gol['GS'],line={'color':'blue'},mode='lines+markers',name='GS'))
        avg_gol_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Gol'})
        st.plotly_chart(go.FigureWidget(data=avg_gol_gr), use_container_width=True)
    if but_h2.button("Casa",icon='🏚️',key='h2'):
        st.text('Media punti stagionale reale vs 3 pnt all time in casa')
        dfh=df_filt[df_filt['C/T']=='C']
        avg_pnth=dfh.groupby('Stagione',as_index=False).agg({'Pnt_real':'mean','Pnt_hyp':'mean'})
        avg_pnth_gr=go.Figure()
        avg_pnth_gr.add_trace(go.Scatter(x=avg_pnth['Stagione'],y=avg_pnth['Pnt_real'],line={'color':'red'},mode='lines+markers',name='Pnt real'))
        avg_pnth_gr.add_trace(go.Scatter(x=avg_pnth['Stagione'],y=avg_pnth['Pnt_hyp'],line={'color':'blue','dash':'dash'},name='Pnt hyp'))
        avg_pnth_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Punti'})
        st.plotly_chart(go.FigureWidget(data=avg_pnth_gr), use_container_width=True)
        st.divider()
        st.text('Media gol fatti stagione per stagione in casa')
        avg_golh = dfh.groupby('Stagione', as_index=False).agg({'GF': 'mean', 'GS': 'mean'})
        avg_golh_gr = go.Figure()
        avg_golh_gr.add_trace(go.Scatter(x=avg_golh['Stagione'],y=avg_golh['GF'],line={'color':'orange'},mode='lines+markers',name='GF'))
        avg_golh_gr.add_trace(go.Scatter(x=avg_golh['Stagione'],y=avg_golh['GS'],line={'color':'blue'},mode='lines+markers',name='GS'))
        avg_golh_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Gol'})
        st.plotly_chart(go.FigureWidget(data=avg_golh_gr), use_container_width=True)
    if but_a2.button("Trasferta",icon="✈️",key='a2'):
        st.text('Media punti stagione per stagione in trasferta')
        dfa=df_filt[df_filt['C/T']=='T']
        avg_pnta=dfa.groupby('Stagione',as_index=False).agg({'Pnt_real':'mean','Pnt_hyp':'mean'})
        avg_pnta_gr=go.Figure()
        avg_pnta_gr.add_trace(go.Scatter(x=avg_pnta['Stagione'],y=avg_pnta['Pnt_real'],line={'color':'red'},mode='lines+markers',name='Pnt real'))
        avg_pnta_gr.add_trace(go.Scatter(x=avg_pnta['Stagione'],y=avg_pnta['Pnt_hyp'],line={'color':'blue','dash':'dash'},name='Pnt hyp'))
        avg_pnta_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Punti'})
        st.plotly_chart(go.FigureWidget(data=avg_pnta_gr), use_container_width=True)
        st.divider()
        st.text('Media gol fatti stagione per stagione in trasferta')
        avg_gola = dfa.groupby('Stagione',as_index=False).agg({'GF':'mean', 'GS': 'mean'})
        avg_gola_gr = go.Figure()
        avg_gola_gr.add_trace(go.Scatter(x=avg_gola['Stagione'],y=avg_gola['GF'],line={'color':'orange'},mode='lines+markers',name='GF'))
        avg_gola_gr.add_trace(go.Scatter(x=avg_gola['Stagione'],y=avg_gola['GS'],line={'color':'blue'},mode='lines+markers',name='GS'))
        avg_gola_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Gol'})
        st.plotly_chart(go.FigureWidget(data=avg_gola_gr), use_container_width=True)

    with st.expander('I migliori marcatori in serie A'):
        st.markdown("*Chi è stato il più grande bomber di tutti i tempi della squadra in Serie A?*")
        marcatori_sq = marcatori[(marcatori['Squadra']==tea_sel) & ((marcatori['Note']!='A') | pd.isna(marcatori['Note']))]
        marcatori_sq['Rig']=[1 if x=='R' else 0 for x in marcatori_sq['Note']]
        m1=marcatori_sq.groupby('Marcatori',as_index=False).agg({'ID':'count','Rig':'sum'})
        m1.columns=['Marcatori','Gol','di cui Rig']
        ass_mar = marcatori_sq.groupby('Assist',as_index=False).agg({'ID':'count'})
        ass_mar.columns=['Marcatori','Assist']
        mar_tot_fin=pd.concat([m1,ass_mar]).groupby('Marcatori',as_index=False).agg({'Gol':'sum','di cui Rig':'sum','Assist':'sum'})
        mar_tot_fin['Gol+Ass']=[x+y for x,y in zip(mar_tot_fin['Gol'],mar_tot_fin['Assist'])]
        mar_tot_fin=mar_tot_fin.sort_values('Gol',ascending=False)
        st.dataframe(mar_tot_fin,hide_index=True)

with rec:
    st.markdown("*Quali sono i record consecutivi per vittorie, sconfitte e molto altro della squadra in Serie A?*")
    but_tot3, but_h3, but_a3 = st.columns(3)
    subc5, subc6 = st.columns(2)
    df1 = match_series_mod(team=tea_sel, choice='Tot')
    df2 = match_series_mod(team=tea_sel, choice='C')
    df3 = match_series_mod(team=tea_sel, choice='T')
    if but_tot3.button("Totale", key='tot3'):
        with subc5:
            st.metric(label='Più lunga striscia di vittorie in totale',value=df1[1])
            st.dataframe(df1[0],hide_index=True)
            st.metric(label='Più lunga striscia di imbattibilità in totale',value=df1[3])
            st.dataframe(df1[2],hide_index=True)
            st.metric(label='Più lunga striscia di prolificità in totale', value=df1[5])
            st.dataframe(df1[4], hide_index=True)
        with subc6:
            st.metric(label='Più lunga striscia di sconfitte in totale', value=df1[7])
            st.dataframe(df1[6], hide_index=True)
            st.metric(label='Più lunga striscia di non vittorie in totale',value=df1[9])
            st.dataframe(df1[8],hide_index=True)
            st.metric(label='Più lunga striscia di clean sheets in totale', value=df1[11])
            st.dataframe(df1[10], hide_index=True)
    if but_h3.button("Casa" ,icon='🏚️', key='h3'):
        with subc5:
            st.metric(label='Più lunga striscia di vittorie in totale',value=df2[1])
            st.dataframe(df2[0],hide_index=True)
            st.metric(label='Più lunga striscia di imbattibilità in totale',value=df2[3])
            st.dataframe(df2[2],hide_index=True)
            st.metric(label='Più lunga striscia di prolificità in totale', value=df2[5])
            st.dataframe(df2[4], hide_index=True)
        with subc6:
            st.metric(label='Più lunga striscia di sconfitte in totale', value=df2[7])
            st.dataframe(df2[6], hide_index=True)
            st.metric(label='Più lunga striscia di non vittorie in totale',value=df2[9])
            st.dataframe(df2[8],hide_index=True)
            st.metric(label='Più lunga striscia di clean sheets in totale', value=df2[11])
            st.dataframe(df2[10], hide_index=True)
    if but_a3.button("Trasferta",icon="✈️", key='a3'):
        with subc5:
            st.metric(label='Più lunga striscia di vittorie in totale',value=df3[1])
            st.dataframe(df3[0],hide_index=True)
            st.metric(label='Più lunga striscia di imbattibilità in totale',value=df3[3])
            st.dataframe(df3[2],hide_index=True)
            st.metric(label='Più lunga striscia di prolificità in totale', value=df3[5])
            st.dataframe(df3[4], hide_index=True)
        with subc6:
            st.metric(label='Più lunga striscia di sconfitte in totale', value=df3[7])
            st.dataframe(df3[6], hide_index=True)
            st.metric(label='Più lunga striscia di non vittorie in totale',value=df3[9])
            st.dataframe(df3[8],hide_index=True)
            st.metric(label='Più lunga striscia di clean sheets in totale', value=df3[11])
            st.dataframe(df3[10], hide_index=True)