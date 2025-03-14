#st.set_page_config(page_title="Serie A - All time",layout='wide')
from Funzioni import *

storico=get_storico()
marcatori=get_marcatori()
riep_part = pd.DataFrame({'Stagioni': list(storico['Stagione']) + list(storico['Stagione']),
                          'Squadre': list(storico['CASA']) + list(storico['TRAS'])})
riep_part = riep_part.drop_duplicates()
riep_grp = riep_part.groupby('Squadre', as_index=False).agg({'Stagioni': 'count'})
riep_grp = riep_grp.sort_values(by='Stagioni')

alb, perp, rec = st.tabs(["Albo d'oro & more",'Classifica perpetua','Record'])
     # stagione corrente

with alb:
    rpl, part = st.columns(2)
    with rpl:
        st.subheader('Partecipazioni Serie A')
        part_gr = go.Figure()
        part_gr.add_trace(go.Bar(y=riep_grp['Squadre'], x=riep_grp['Stagioni'], orientation='h'))
        part_gr.update_layout(height=1200)
        part_gr.update_xaxes(side='top')
        st.plotly_chart(go.FigureWidget(data=part_gr))

        st.divider()

        clas_rbc['Scudetti'] = [int(x) for x in clas_rbc['Scudetti']]
        bcr = barplot(df=clas_rbc, item_column='Squadra', value_column='Scudetti', time_column='Anno')
        rbc = bcr.plot(time_label='Anno', value_label='Scudetti', title='Scudetti vinti', frame_duration=1000)
        st.plotly_chart(rbc)
    with part:
        st.subheader('Albo d\'oro')
        for i in range(0, len(albo), 4):
            cols = st.columns(4)
            for j, (_, row) in enumerate(albo.iloc[i:i + 4].iterrows()):
                with cols[j]:
                    st.image(Image.open(BytesIO(requests.get(row['url_Stemma']).content)),
                             caption=f"{row['Vincitore']} ({row['Stagione']})", use_container_width=True)

with perp:
    st.subheader('Classifica perpetua')
    st.markdown("*Quale squadra ha la maggiore media punti in Serie A?*")
    pclass=ranking(dati=storico,seas='All').drop('Rk',axis=1)
    st.dataframe(pclass, hide_index=True)
    st.divider()
    perp1, perp2=st.columns([2,1])
    with perp1:
        st.subheader('Classifica marcatori all time')
        st.markdown('*Chi sono i bomber storici in Serie A?*')
        marcatori_alt = marcatori[((marcatori['Note'] != 'A') | pd.isna(marcatori['Note']))]
        marcatori_alt['Rig'] = [1 if x == 'R' else 0 for x in marcatori_alt['Note']]
        m1 = marcatori_alt.groupby('Marcatori', as_index=False).agg({ 'ID': 'count', 'Rig': 'sum','Squadra': list})
        m1.columns = ['Marcatori', 'Gol', 'di cui Rig','Squadra']
        ass_mar = marcatori_alt.groupby('Assist', as_index=False).agg({'ID': 'count'})
        ass_mar.columns = ['Marcatori', 'Assist']
        mar_alt_fin = m1.merge(ass_mar, how='left', on='Marcatori')
        mar_alt_fin['Assist'] = mar_alt_fin['Assist'].fillna(0)
        mar_alt_fin['Gol+Ass'] = [x + y for x, y in zip(mar_alt_fin['Gol'], mar_alt_fin['Assist'])]
        mar_alt_fin = mar_alt_fin.sort_values('Gol', ascending=False)
        mar_alt_fin['Squadra'] = [sorted(set(x)) for x in mar_alt_fin['Squadra']]
        mar_alt_fin['Squadra'] = mar_alt_fin['Squadra'].apply(lambda x: ', '.join(map(str, x)))
        st.dataframe(mar_alt_fin, hide_index=True)
    with perp2:
        st.subheader('Classifica autogol all time')
        st.markdown("*Chi il più sfortunato nella storia della Serie A?*")
        autogols = marcatori[marcatori['Note'] == 'A']
        autogols = autogols.groupby('Marcatori', as_index=False).agg({'ID': 'count'})
        autogols.columns = ['Giocatore', 'Autogol']
        autogols = autogols.sort_values('Autogol', ascending=False)
        st.dataframe(autogols, hide_index=True)
    st.divider()
    st.subheader('Classifica allenatori all time')
    st.dataframe(mister_alltime(dati=storico,team='All'), hide_index=True)

    with st.expander('Media gol stagionale'):
        st.markdown("*E' vero che negli anni 70 e 80 si segnava di meno?*")
        storico['Gol Tot']=[x+y for x,y in zip(storico['GC'],storico['GT'])]
        dfg=storico.groupby('Stagione',as_index=False).agg({'Gol Tot':'mean'})
        df_gr = px.line(dfg, x="Stagione", y="Gol Tot", markers=True)
        df_gr.update_layout(xaxis=dict(title="Stagione", type="category"),yaxis=dict(title="Media Gol"))
        st.plotly_chart(df_gr)
    with st.expander('Vittorie C/T stagionale'):
        st.markdown("*Com'è cambiato il fattore campo stagione dopo stagione?*")
        storico['WH']=[100 if x>y else 0 for x,y in zip(storico['GC'],storico['GT'])]
        storico['WA'] = [100 if x < y else 0 for x, y in zip(storico['GC'], storico['GT'])]
        storico['N'] = [100 if x == y else 0 for x, y in zip(storico['GC'], storico['GT'])]
        dfg1 = storico.groupby('Stagione', as_index=False).agg({'WH': 'mean','WA':'mean','N':'mean'})
        dfg1_gr = px.bar(dfg1, x="Stagione", y=['WH','N','WA'])
        dfg1_gr.update_layout(xaxis=dict(title="Stagione", type="category"),yaxis=dict(title="% W H/A"))
        st.plotly_chart(dfg1_gr)
    with st.expander('Gol 1/2 Tempo'):
        st.markdown("*Si è sempre segnato di più nel secondo tempo rispetto al primo?*")
        marcatori['Stagione']=[x[:4]+'-'+x[4:6] for x in marcatori['ID']]
        marcatori['Gol 1T']=[100 if x<=45 else 0 for x in marcatori['Minuto']]
        marcatori['Gol 2T'] = [100 if x > 45 else 0 for x in marcatori['Minuto']]
        df2=marcatori.groupby(['Stagione'],as_index=False).agg({'Gol 1T':'mean','Gol 2T':'mean'})
        df2_gr = px.bar(df2, x="Stagione", y=['Gol 1T','Gol 2T'])
        df2_gr.update_layout(xaxis=dict(title="Stagione", type="category"), yaxis=dict(title="% Gol 1T/2T"))
        st.plotly_chart(df2_gr)

with rec:
    st.markdown("*Record tutt'ora imbattuti in Serie A*")
    storico['diff_gol']=[x-y for x,y in zip(storico['GC'],storico['GT'])]
    storico['sum_gol'] = [x + y for x, y in zip(storico['GC'], storico['GT'])]
    dfs=storico.sort_values('diff_gol')
    dfg = storico.sort_values('sum_gol',ascending=False)
    wmore = dfg.iloc[0, :]
    wt=dfs.iloc[0,:]
    wc = dfs.iloc[dfs.shape[0]-1, :]
    daymore=storico.groupby(['Stagione','Giornata'],as_index=False).agg({'sum_gol':'sum'})
    daymore1 = daymore.sort_values('sum_gol', ascending=False)
    dm = daymore1.iloc[0, :]
    st.write(f"Vittoria più larga in casa: {wc['CASA']} - {wc['TRAS']} {wc['GC'].item()}-{wc['GT'].item()} - {wc['Giornata'].item()}° giornata - {wc['Giorno']}")
    st.write(f"Vittoria più larga in trasferta: {wt['CASA']} - {wt['TRAS']} {wt['GC'].item()}-{wt['GT'].item()} - {wt['Giornata'].item()}° giornata - {wt['Giorno']}")
    st.write(f"Partita con più gol: {wmore['CASA']} - {wmore['TRAS']} {wmore['GC'].item()}-{wmore['GT'].item()} - {wmore['Giornata'].item()}° giornata - {wmore['Giorno']}")
    st.write(f"Giornata con più gol: {dm['Giornata'].item()}° giornata della stagione {dm['Stagione']} con {dm['sum_gol'].item()} gol")
