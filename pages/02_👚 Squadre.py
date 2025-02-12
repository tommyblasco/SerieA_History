import pandas as pd
import streamlit

from Funzioni import *

tea_sel=st.selectbox('Seleziona una squadra',lista_sq)

titcol1, titcol2 = st.columns([2, 1])
with titcol1:
    st.header(tea_sel)
with titcol2:
    st.image(Image.open(BytesIO(requests.get(load_images(team=tea_sel,yyyy='2999')).content)))

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
    pos_gr.update_layout(xaxis={'title':'Stagione','type':'category','autorange':'reversed'}, yaxis={'title':'Stagione','range':[21,0]})
    st.plotly_chart(pos_gr)

st.divider()

st.subheader('Bilancio serie A')
df_casa=storico[storico['CASA']==tea_sel]
df_tras=storico[storico['TRAS']==tea_sel]
met_casa = [df_casa.shape[0], df_casa[df_casa['GC']>df_casa['GT']].shape[0], df_casa[df_casa['GC']==df_casa['GT']].shape[0],
            df_casa[df_casa['GC']<df_casa['GT']].shape[0], sum(df_casa['GC']), sum(df_casa['GT'])]
met_tras = [df_tras.shape[0], df_tras[df_tras['GC']<df_tras['GT']].shape[0], df_tras[df_tras['GC']==df_tras['GT']].shape[0],
            df_tras[df_tras['GC']>df_tras['GT']].shape[0], sum(df_tras['GT']), sum(df_tras['GC'])]
but_tot, but_h, but_a = st.columns(3)
subc1, subc2, subc3, subc4 = st.columns(4)
ssc1, ssc2 = st.columns(2)
if but_tot.button('Totale'):
    subc1.metric(label='Giocate', value=met_casa[0]+met_tras[0],border=True)
    subc2.metric(label='Vinte', value=met_casa[1] + met_tras[1],border=True)
    subc3.metric(label='Pareggiate', value=met_casa[2] + met_tras[2],border=True)
    subc4.metric(label='Perse', value=met_casa[3] + met_tras[3],border=True)
    with ssc1:
        tot_bil_pie = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[met_casa[1]+met_tras[1], met_casa[2]+met_tras[2], met_casa[3]+met_tras[3]],
                       labels=["W", "D","L"])
        st.plotly_chart(go.FigureWidget(data=tot_bil_pie), use_container_width=True)
        st.metric(label='Bilancio', value=met_casa[1] + met_tras[1] - met_casa[3] - met_tras[3], border=True)
    with ssc2:
        tot_g_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                            values=[met_tras[4]+met_casa[4], met_tras[5]+met_casa[5]],
                            labels=["GF", "GS"])
        st.plotly_chart(go.FigureWidget(data=tot_g_pie), use_container_width=True)
if but_h.button('Casa',icon='🏚️'):
    subc1.metric(label='Giocate',value=met_casa[0],border=True)
    subc2.metric(label='Vinte', value=met_casa[1],border=True)
    subc3.metric(label='Pareggiate', value=met_casa[2],border=True)
    subc4.metric(label='Perse', value=met_casa[3],border=True)
    with ssc1:
        home_bil_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                             values=[met_casa[1], met_casa[2], met_casa[3]],
                             labels=["W", "D", "L"])
        st.plotly_chart(go.FigureWidget(data=home_bil_pie), use_container_width=True)
        st.metric(label='Bilancio', value=met_casa[1] - met_casa[3], border=True)
    with ssc2:
        home_g_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                              values=[met_casa[4], met_casa[5]],
                              labels=["GF", "GS"])
        st.plotly_chart(go.FigureWidget(data=home_g_pie), use_container_width=True)
if but_a.button('Trasferta',icon='✈️'):
    subc1.metric(label='Giocate',value=met_tras[0],border=True)
    subc2.metric(label='Vinte', value=met_tras[1],border=True)
    subc3.metric(label='Pareggiate', value=met_tras[2],border=True)
    subc4.metric(label='Perse', value=met_tras[3],border=True)
    with ssc1:
        away_bil_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                             values=[met_tras[1],met_tras[2],met_tras[3]],
                             labels=["W", "D", "L"])
        st.plotly_chart(go.FigureWidget(data=away_bil_pie), use_container_width=True)
        st.metric(label='Bilancio', value=met_tras[1] - met_tras[3], border=True)
    with ssc2:
        away_g_pie = go.Pie(hole=0.5, sort=False, direction='clockwise',
                            values=[met_tras[4], met_tras[5]],
                            labels=["GF", "GS"])
        st.plotly_chart(go.FigureWidget(data=away_g_pie), use_container_width=True)

