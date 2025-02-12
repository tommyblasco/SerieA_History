import pandas as pd
import streamlit

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
    met_casa = [df_casa.shape[0], df_casa[df_casa['GC']>df_casa['GT']].shape[0], df_casa[df_casa['GC']==df_casa['GT']].shape[0],
                df_casa[df_casa['GC']<df_casa['GT']].shape[0], sum(df_casa['GC']), sum(df_casa['GT'])]
    met_tras = [df_tras.shape[0], df_tras[df_tras['GC']<df_tras['GT']].shape[0], df_tras[df_tras['GC']==df_tras['GT']].shape[0],
                df_tras[df_tras['GC']>df_tras['GT']].shape[0], sum(df_tras['GT']), sum(df_tras['GC'])]
    but_tot, but_h, but_a = st.columns(3)
    subc1, subc2, subc3, subc4 = st.columns(4)
    ssc1, ssc2 = st.columns(2)
    if but_tot.button('Totale'):
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
    if but_h.button('Casa',icon='🏚️'):
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
    if but_a.button('Trasferta',icon='✈️'):
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
    df_tras_filt['C/T'] = ['C'] * df_tras_filt.shape[0]
    df_filt = pd.concat([df_casa_filt,df_tras_filt],ignore_index=True)
    df_filt['Pnt_real']=[3 if (x>y) & (z>='1994-95') else 2 if (x>y) & (z<'1994-95') else 1 if x==y else 0 for x,y,z in zip(df_filt['GF'],df_filt['GS'],df_filt['Stagione'])]
    df_filt['Pnt_hyp']=[3 if (x>y) & (z<'1994-95') else 1 if (x==y) & (z<'1994-95') else 0 if z<'1994-95' else np.nan for x,y,z in zip(df_filt['GF'],df_filt['GS'],df_filt['Stagione'])]

    tot_h_a = st.pills('Scegli:'["Totale","Casa","Trasferta"])
    col_ins_1, col_ins_2 = st.columns(2)

    if tot_h_a=="Totale":
        with col_ins_1:
            st.text('Media punti stagionale reale vs 3 pnt all time')
            avg_pnt=df_filt.groupby('Stagione',as_index=False).agg({'Pnt_real':'mean','Pnt_hyp':'mean'})
            avg_pnt_gr=go.Figure()
            avg_pnt_gr.add_trace(go.Scatter(x=avg_pnt['Stagione'],y=avg_pnt['Pnt_real'],line={'color':'orange','mode':'lines+markers'}))
            avg_pnt_gr.add_trace(go.Scatter(x=avg_pnt['Stagione'],y=avg_pnt['Pnt_hyp'],line={'color':'blue','dash':'dash'}))
            avg_pnt_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Punti'})
            st.plotly_chart(go.FigureWidget(data=avg_pnt_gr), use_container_width=True)
        with col_ins_2:
            st.text('Media gol fatti/subiti stagionale')
            avg_gol = df_filt.groupby('Stagione',as_index=False).agg({'GF':'mean','GS':'mean'})
            avg_gol_gr = go.Figure()
            avg_gol_gr.add_trace(go.Scatter(x=avg_gol['Stagione'],y=avg_gol['GF'],line={'color':'orange','mode':'lines+markers'}))
            avg_gol_gr.add_trace(go.Scatter(x=avg_gol['Stagione'],y=avg_gol['GS'],line={'color':'blue','mode':'lines+markers'}))
            avg_gol_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Gol'})
            st.plotly_chart(go.FigureWidget(data=avg_gol_gr), use_container_width=True)
    elif tot_h_a=="Casa":
        with col_ins_1:
            st.text('Media punti stagionale reale vs 3 pnt all time in casa')
            dfh=df_filt[df_filt['C/T']=='C']
            avg_pnth=dfh.groupby('Stagione',as_index=False).agg({'Pnt_real':'mean','Pnt_hyp':'mean'})
            avg_pnth_gr=go.Figure()
            avg_pnth_gr.add_trace(go.Scatter(x=avg_pnth['Stagione'],y=avg_pnth['Pnt_real'],line={'color':'red','mode':'lines+markers'}))
            avg_pnth_gr.add_trace(go.Scatter(x=avg_pnth['Stagione'],y=avg_pnth['Pnt_hyp'],line={'color':'blue','dash':'dash'}))
            avg_pnth_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Punti'})
            st.plotly_chart(go.FigureWidget(data=avg_pnth_gr), use_container_width=True)
        with col_ins_2:
            st.text('Media gol fatti stagione per stagione in casa')
            avg_golh = dfh.groupby('Stagione', as_index=False).agg({'GF': 'mean', 'GS': 'mean'})
            avg_golh_gr = go.Figure()
            avg_golh_gr.add_trace(go.Scatter(x=avg_golh['Stagione'],y=avg_golh['GF'],line={'color':'orange','mode':'lines+markers'}))
            avg_golh_gr.add_trace(go.Scatter(x=avg_golh['Stagione'],y=avg_golh['GS'],line={'color':'blue','mode':'lines+markers'}))
            avg_golh_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Gol'})
            st.plotly_chart(go.FigureWidget(data=avg_golh_gr), use_container_width=True)
    elif tot_h_a=="Trasferta":
        with col_ins_1:
            st.text('Media punti stagione per stagione in trasferta')
            dfa=df_filt[df_filt['C/T']=='T']
            avg_pnta=dfa.groupby('Stagione',as_index=False).agg({'Pnt_real':'mean','Pnt_hyp':'mean'})
            avg_pnta_gr=go.Figure()
            avg_pnta_gr.add_trace(go.Scatter(x=avg_pnta['Stagione'],y=avg_pnta['Pnt_real'],line={'color':'red','mode':'lines+markers'}))
            avg_pnta_gr.add_trace(go.Scatter(x=avg_pnta['Stagione'],y=avg_pnta['Pnt_hyp'],line={'color':'blue','dash':'dash'}))
            avg_pnta_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Punti'})
            st.plotly_chart(go.FigureWidget(data=avg_pnta_gr), use_container_width=True)
        with col_ins_2:
            st.text('Media gol fatti stagione per stagione in trasferta')
            avg_gola = dfa.groupby('Stagione',as_index=False).agg({'GF':'mean', 'GS': 'mean'})
            avg_gola_gr = go.Figure()
            avg_gola_gr.add_trace(go.Scatter(x=avg_gola['Stagione'],y=avg_gola['GF'],line={'color':'orange','mode':'lines+markers'}))
            avg_gola_gr.add_trace(go.Scatter(x=avg_gola['Stagione'],y=avg_gola['GS'],line={'color':'blue','mode':'lines+markers'}))
            avg_gola_gr.update_layout(xaxis={'title':'Stagione','type':'category'}, yaxis={'title':'Media Gol'})
            st.plotly_chart(go.FigureWidget(data=avg_gola_gr), use_container_width=True)