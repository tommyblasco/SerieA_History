from Funzioni import *
import pandas as pd

premierleague = st.session_state.premierleague.copy()
laliga = st.session_state.laliga.copy()
ligue1 = st.session_state.ligue1.copy()
bundesliga = st.session_state.bundesliga.copy()

st.header("In giro per l'Europa")

league_sel=st.selectbox('Seleziona una lega',["Premier League","La Liga","Bundesliga","Ligue 1"])
db_lega = {'Premier League':premierleague,'La Liga':laliga,'Bundesliga':bundesliga,'Ligue 1':ligue1}
db=db_lega[league_sel]
n_gio = max(db['Giornata'])
lista_sq=sorted(set(list(db['CASA'])+list(db['TRAS'])))

risclass, prec = st.tabs(['Risultati e classifica','Precedenti'])
with risclass:
    class_c, ris_c = st.columns([2, 1])
    with class_c:
        stagione_sel = st.selectbox('Seleziona una stagione', sorted(set(list(db['Stagione'])), reverse=True))
        classifica = ranking_short(db=db, league_name=league_sel, seas=stagione_sel)
        st.dataframe(classifica,hide_index=True)
    with ris_c:
        if n_gio==1:
            sel_gio = st.slider("Seleziona la giornata:",1,2,n_gio)
        else:
            sel_gio = st.slider("Seleziona la giornata:", 1, n_gio, n_gio)
        db['Risultato']=[str(x)+'-'+str(y) for x,y in zip(db['GC'],db['GT'])]
        df_fil_gio=db[db['Giornata']==sel_gio]
        df_fil_gio=df_fil_gio.sort_values(['Data','CASA'])
        df_fil_gio['Giorno'] = df_fil_gio['Data'].strftime('%b %d, %Y')
        st.dataframe(df_fil_gio[['Giorno','CASA','TRAS','Risultato']],hide_index=True)

with prec:
    st.markdown(f"*Chi ha vinto di più in {league_sel} tra le 2 squadre?*")
    colt1, colt2 = st.columns(2)
    with colt1:
        t1 = st.selectbox('Seleziona il team 1:', lista_sq)
    with colt2:
        lsq2 = sorted(
            set(list(db.loc[db['CASA'] == t1, 'TRAS']) + list(db.loc[db['TRAS'] == t1, 'CASA'])))
        t2 = st.selectbox('Seleziona il team 2:', lsq2)
    df1 = prec(dati=db, t1=t1, t2=t2)[0]
    df2 = prec(dati=db, t1=t1, t2=t2)[1]
    if (df1.shape[0] == 0) | (df2.shape[0] == 0):
        st.error('Nessun precedente trovato')
    else:
        wt1 = df1['WH'].item() + df2['WA'].item()
        wt2 = df2['WH'].item() + df1['WA'].item()
        n_gio = df1['TRAS'].item() + df2['TRAS'].item()
        pareg = df1['N'].item() + df2['N'].item()
        st.dataframe(pd.DataFrame({
            'Squadra':[f'home {t1}',f'home {t2}','Totale'],
            'Giocate':[df1['TRAS'].item(), df2['TRAS'].item(), n_gio],
            f'W {t1}':[df1['WH'].item(),df2['WA'].item(),wt1],
            'N':[df1['N'].item(),df2['N'].item(),pareg],
            f'W {t2}':[df2['WH'].item(),df1['WA'].item(),wt2]}),hide_index=True)

    st.subheader('Andamento precedenti nel tempo')
    st.markdown("*Chi era solito vincere nel passato tra i 2 team?*")
    pre_cum = prec(dati=db, t1=t1, t2=t2)[2]
    cump_gr = px.area(pre_cum, x="Stagione", y="CumPr", markers=True)
    cump_gr.update_layout(xaxis=dict(title="Stagione", type="category"))
    cump_gr.add_annotation(x=-0.2, y=max(pre_cum["CumPr"]), showarrow=False,
                           text=f"{t1}", yref="y")
    cump_gr.add_annotation(x=-0.2, y=min(pre_cum["CumPr"]), showarrow=False,
                           text=f"{t2}", yref="y")
    st.plotly_chart(cump_gr)
