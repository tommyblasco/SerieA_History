#st.set_page_config(page_title="Serie A - Stagioni",layout='wide')
from Home import load_data
from Funzioni import *


storico=get_storico()
marcatori=get_marcatori()
seas_list = sorted(set(storico['Stagione']),reverse=True)

st.header('Le stagioni')

sea_sel=st.selectbox('Seleziona una stagione',seas_list)

df=storico[storico['Stagione']==sea_sel]
start_sea=min(df['Data'])
end_sea=max(df['Data'])
n_gio=max(df['Giornata'])

rc, mgol, ins, sm = st.tabs(['Risultati e classifica','Marcatori & gol stats','Insights','Special matches'])
with rc:
    class_c, ris_c = st.columns([2, 1])
    with class_c:
        sel_date = st.slider("Seleziona il range di date:", min_value=start_sea, max_value=end_sea,value=(start_sea,end_sea),step=timedelta(days=1),format="DD/MM/YYYY")
        classifica=ranking(dati=storico,seas=sea_sel,st_date=sel_date[0],en_date=sel_date[1])
        stem = []
        for s in classifica['Squadra']:
            stem.append(load_images(team=s, yyyy=sea_sel[:4]))
        classifica.insert(1,"Badge",stem)
        st.dataframe(classifica,column_config={"Badge":st.column_config.ImageColumn()},hide_index=True)
    with ris_c:
        sel_gio = st.slider("Seleziona la giornata:",1,n_gio,n_gio)
        df['Risultato']=[str(x)+'-'+str(y) for x,y in zip(df['GC'],df['GT'])]
        df_fil_gio=df[df['Giornata']==sel_gio]
        df_fil_gio=df_fil_gio.sort_values(['Data','CASA'])
        st.dataframe(df_fil_gio[['Giorno','CASA','TRAS','Risultato']],hide_index=True)

    with st.expander('Andamento classifica'):
        st.markdown("*Come si è evoluta la classifica giornata per giornata?*")
        c_cum=class_cum(dati=storico,seas=sea_sel)
        cum_gr = px.line(c_cum, x="Giornata", y="CumP", color="Squadra",markers=True)
        cum_gr.update_layout(xaxis_title="Giornata", yaxis_title="Punti Cumulati")
        st.plotly_chart(cum_gr)

    with st.expander('Classifica casa/trasferta'):
        clh, cla = st.columns(2)
        with clh:
            st.write('Classifica in casa:')
            st.dataframe(class_ct(dati=storico,seas=sea_sel)[0],hide_index=True)
        with cla:
            st.write('Classifica in trasferta:')
            st.dataframe(class_ct(dati=storico,seas=sea_sel)[1],hide_index=True)

    with st.expander('Classifica 1° Tempo e esito 1°/2° tempo'):
        cl1t, cles12 = st.columns(2)
        with cl1t:
            st.markdown("*Come sarebbe la classifica se le partite finissero entro i primi 45'?*")
            st.dataframe(class_1t(datis=storico,datim=marcatori,seas=sea_sel),hide_index=True)
        with cles12:
            st.markdown("*Il risultato del primo tempo è cambiato o rimasto invariato nel secondo?*")
            st.dataframe(change_1t_2t(datis=storico,datim=marcatori,seas=sea_sel))

with mgol:
    id_eligibles = [x for x in marcatori['ID'] if x[:4]==sea_sel[:4]]
    marcatori_st = marcatori[(marcatori['ID'].isin(id_eligibles)) & ((marcatori['Note'] != 'A') | pd.isna(marcatori['Note']))]
    marcatori_st['Rig'] = [1 if x == 'R' else 0 for x in marcatori_st['Note']]
    m1 = marcatori_st.groupby('Marcatori', as_index=False).agg({'Squadra':list,'ID': 'count', 'Rig': 'sum'})
    m1.columns = ['Marcatori', 'Squadra','Gol', 'di cui Rig']
    ass_mar = marcatori_st.groupby('Assist', as_index=False).agg({'ID': 'count'})
    ass_mar.columns = ['Marcatori','Assist']
    mar_tot_fin = m1.merge(ass_mar,how='left',on='Marcatori')
    mar_tot_fin['Assist']=mar_tot_fin['Assist'].fillna(0)
    mar_tot_fin['Gol+Ass'] = [x + y for x, y in zip(mar_tot_fin['Gol'], mar_tot_fin['Assist'])]
    mar_tot_fin = mar_tot_fin.sort_values('Gol', ascending=False)
    mar_tot_fin['Squadra'] = [sorted(set(x)) for x in mar_tot_fin['Squadra']]
    mar_tot_fin['Squadra'] = mar_tot_fin['Squadra'].apply(lambda x: ', '.join(map(str, x)))
    m1,m2 = st.columns([2,1])
    with m1:
        st.subheader('Classifica marcatori')
        st.dataframe(mar_tot_fin, hide_index=True)
    with m2:
        played = df.shape[0]
        gol_tot = sum(df['GC']) + sum(df['GT'])
        st.metric(label='Gol segnati in stagione', value=gol_tot)
        media_gol = round(gol_tot / played, 2)
        st.metric(label='Media gol a partita', value=media_gol)

    st.divider()

    piegol1, piegol2 = st.columns(2)
    with piegol1:
        st.markdown("*Quanti gol sono stati segnati in casa e in trasferta?*")
        gca = sum(df['GC'])
        gtr = sum(df['GT'])
        gct = go.Figure(go.Pie(hole=0.5, sort=False, direction='clockwise', values=[gca, gtr],
                     labels=["Gol Casa", "Gol Tras"]))
        gct.update_layout(annotations=[dict(text=f'{gca+gtr} gol',x=0.5, y=0.5, font_size=15, showarrow=False,xanchor='center')])
        st.plotly_chart(go.FigureWidget(data=gct), use_container_width=True)

        st.markdown("*Quanti gol sono stati segnati per partita?*")
        n_gol = [x + y for x, y in zip(df['GC'], df['GT'])]
        dis_gol = go.Figure()
        dis_gol.add_trace(go.Histogram(x=n_gol, name="count"))
        st.plotly_chart(go.FigureWidget(data=dis_gol), use_container_width=True)
    with piegol2:
        st.markdown("*In quale frazione di tempo vengono segnati più gol?*")
        marcatori_st['Tempo'] = ['1T' if x <= 45 else '2T' for x in marcatori_st['Minuto']]
        marcatori_st['Q_Tempo'] = ['0-15' if (0 < x <= 15) | (45 < x <= 60) else '16-30' if (15 < x <= 30) | (60 < x <= 75) else '31-45' for x in marcatori_st['Minuto']]
        df_pivot = marcatori_st.pivot_table(index='Tempo', columns='Q_Tempo', values='Marcatori', aggfunc='count')
        df_freq = df_pivot * 100 / df.shape[0]
        time_gr = go.Figure(data=go.Heatmap(z=df_freq.values, x=df_freq.columns, y=df_freq.index,
                                           text=df_freq.round(1).astype(str) + '%', texttemplate="%{text}",
                                           colorscale="oranges", showscale=True))
        time_gr.update_layout(xaxis=dict(title="Segmento temporale", type="category"),
                             yaxis=dict(title="1°/2° Tempo", type="category", autorange="reversed"))
        time_gr.update_xaxes(side='top')
        st.plotly_chart(go.FigureWidget(data=time_gr), use_container_width=True)


with ins:
    pie1, pie2 = st.columns(2)
    with pie1:
        st.markdown("*Quante partite sono state vinte in casa e in trasferta? Quanti pareggi?*")
        wh=df[df['GC']>df['GT']].shape[0]
        wa = df[df['GC'] < df['GT']].shape[0]
        wh_d_wa = go.Figure(go.Pie(hole=0.5, sort=False, direction='clockwise', values=[wh, played-wh-wa, wa],
                        labels=["W Casa","Pari", "W Tras"]))
        wh_d_wa.update_layout(annotations=[dict(text=f'{played} partite',x=0.5, y=0.5, font_size=15, showarrow=False,xanchor='center')])
        st.plotly_chart(go.FigureWidget(data=wh_d_wa), use_container_width=True)

    with pie2:
        st.markdown("*Quante partite hanno avuto meno o più di ... gol?*")
        un_ov = st.slider("Seleziona la soglia U/O:", min_value=0.5, max_value=5.5, value=2.5)
        over = [x + y for x, y in zip(df['GC'], df['GT']) if x + y > un_ov]
        under = [x + y for x, y in zip(df['GC'], df['GT']) if x + y < un_ov]
        uo_gr = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[len(under), len(over)],
                       labels=["Under", "Over"])
        st.plotly_chart(go.FigureWidget(data=uo_gr), use_container_width=True)

    with st.expander('Frequenza risultati'):
        st.markdown("*Quali risultati si sono verificati più frequentemente?*")
        st.write("Per riga: Gol segnati in casa, per colonna: gol segnati in trasferta")
        df['clus_GC']=[str(x) if x<=4 else '>4' for x in df['GC']]
        df['clus_GT'] = [str(x) if x <= 4 else '>4' for x in df['GT']]
        df_pivot = df.pivot_table(index='clus_GC', columns='clus_GT', values='GC', aggfunc='count')
        df_freq = df_pivot*100/df.shape[0]
        df_freq=df_freq.fillna(0)
        res_gr = go.Figure(data=go.Heatmap( z=df_freq.values, x=df_freq.columns, y=df_freq.index,
            text=df_freq.round(1).astype(str) + '%', texttemplate="%{text}",
            colorscale="blues", showscale=True))
        res_gr.update_layout(xaxis=dict(title="Gol Tras", type="category"),yaxis=dict(title="Gol Casa", type="category"))
        res_gr.update_xaxes(side='top')
        st.plotly_chart(go.FigureWidget(data=res_gr), use_container_width=True)

    with st.expander('Andamento gol per giornata'):
        st.markdown("*Quanti gol in media sono stati segnati per giornata?*")
        df['gol_match'] = [x + y for x, y in zip(df['GC'], df['GT'])]
        agg_gol_gio=df.groupby(['Giornata'],as_index=False).agg({'gol_match':'mean'})
        gol_gio_gr = px.line(agg_gol_gio, x="Giornata", y="gol_match", markers=True)
        gol_gio_gr.update_layout(xaxis_title="Giornata", yaxis_title="Media gol segnati")
        st.plotly_chart(gol_gio_gr)

    with st.expander('Minuti in vantaggio'):
        st.markdown("*Quanti minuti (riparametrati su 90') in media, le squadre hanno passato in vantaggio/svantaggio/pareggio?*")
        df_min_adv = min_advantage(datis=storico,datim=marcatori,seas=sea_sel)
        hbaradv = go.Figure()
        hbaradv.add_trace(go.Bar(x=df_min_adv['Vantaggio'], y=df_min_adv['Squadre'], orientation='h', marker=dict(color='green'),
                                text=df_min_adv['Vantaggio']))
        hbaradv.add_trace(go.Bar(x=df_min_adv['Pareggio'], y=df_min_adv['Squadre'], orientation='h', marker=dict(color='gray'),
                                text=df_min_adv['Pareggio']))
        hbaradv.add_trace(go.Bar(x=df_min_adv['Svantaggio'], y=df_min_adv['Squadre'], orientation='h', marker=dict(color='red'),
                                text=df_min_adv['Svantaggio']))
        hbaradv.update_layout(barmode='stack', showlegend=False, height=1600, xaxis=dict(side='top'), yaxis=dict(autorange='reversed'))
        hbaradv.update_traces(textangle=0)
        st.plotly_chart(hbaradv)

with sm:
    st.subheader('Ricerca partita:')
    st.markdown("*Conosci risultato e marcatori di qualsiasi partita in stagione*")
    mat_cas, mat_tra=st.columns(2)
    with mat_cas:
        l1=sorted(list(classifica['Squadra']))
        ht=st.selectbox('Seleziona la squadra in casa',l1)
    with mat_tra:
        l2=[x for x in l1 if x!=ht]
        at=st.selectbox('Seleziona la squadra in trasferta',l2)

    search_match=df[(df['CASA']==ht) & (df['TRAS']==at)]
    #stcol, nomcol, riscol, infcol = st.columns([2,2,2,1])

    if search_match.shape[0]>0:
        st.write(f"{search_match['Giornata'].item()}° giornata - {search_match['Giorno'].item()} ")
        logo1 = base64.b64encode(BytesIO(requests.get(load_images(team=ht, yyyy=sea_sel)).content).read()).decode()
        logo2 = base64.b64encode(BytesIO(requests.get(load_images(team=at, yyyy=sea_sel)).content).read()).decode()

        tabellino = go.Figure(
            layout=go.Layout(
                xaxis=dict(range=[0, 2], showgrid=False, zeroline=False, visible=False),
                yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
                plot_bgcolor='black',
                shapes=[
                    dict(type="rect", x0=0, y0=0, x1=1, y1=1,
                         line=dict(width=2, color='white'), fillcolor='purple', layer="below"),
                    dict(type="rect", x0=1, y0=0, x1=2, y1=1,
                         line=dict(width=2, color='white'), fillcolor='yellow', layer="below"),
                ]
                ,images=[
                    dict(source=f'data:image/png;base64,{logo1}', x=0.05, y=0.5, xref="x", yref="y",
                         sizex=0.2, sizey=0.4, xanchor="left", yanchor="middle"),
                    dict(source=f'data:image/png;base64,{logo2}', x=1.95, y=0.5, xref="x", yref="y",
                         sizex=0.2, sizey=0.4, xanchor="right", yanchor="middle"),
                ]
            )
        )
        tabellino.add_trace(go.Scatter(x=[0.9], y=[0.5], text=str(search_match['GC'].item()), mode="text",
            textfont=dict(size=50, color='white', family='Arial Black')))

        tabellino.add_trace(go.Scatter(x=[0.5], y=[0.5], text=search_match['CASA'].item(), mode="text",
            textfont=dict(size=20, color='white', family='Arial Black')))

        tabellino.add_trace(go.Scatter(x=[1.1], y=[0.5], text=str(search_match['GT'].item()), mode="text",
            textfont=dict(size=50, color='white', family='Arial Black')))

        tabellino.add_trace(go.Scatter(x=[1.5], y=[0.5], text=search_match['TRAS'].item(), mode="text",
            textfont=dict(size=20, color='white', family='Arial Black'), textposition="middle right"))
        st.plotly_chart(tabellino)

        if search_match['GC'].item() + search_match['GT'].item() > 0:
            idm = search_match['ID'].item()
            scorers = marcatori[marcatori['ID'] == idm]
            scorers=scorers.sort_values(['Minuto','Recupero'])
            scorers.reset_index(drop=True, inplace=True)
            shome = scorers[scorers['Squadra'] == ht]
            saway = scorers[scorers['Squadra'] == at]
            mat_cas1, mat_tra1 = st.columns(2)
            with mat_cas1:
                if shome.shape[0]>0:
                    for s in list(range(shome.shape[0])):
                        nome_scor = shome.iloc[s, 0]
                        nome_split = nome_scor.split(' ')
                        nome_fin = '. '.join([x if x.isupper() else x[:1] for x in nome_split])
                        if (pd.notna(shome.iloc[s, 2])) & (pd.notna(shome.iloc[s, 3])):
                            st.write(
                                f"{shome.iloc[s, 1]}'+{shome.iloc[s, 2]} ({shome.iloc[s, 3]}) {nome_fin} ({shome.iloc[s, 5][:1]})")
                        elif (pd.notna(shome.iloc[s, 2])) & (pd.isna(shome.iloc[s, 3])):
                            st.write(
                                f"{shome.iloc[s, 1]}'+{shome.iloc[s, 2]} {nome_fin} ({shome.iloc[s, 5][:1]})")
                        elif (pd.isna(shome.iloc[s, 2])) & (pd.notna(shome.iloc[s, 3])):
                            st.write(
                                f"{shome.iloc[s, 1]}' ({shome.iloc[s, 3]}) {nome_fin} ({shome.iloc[s, 5][:1]})")
                        else:
                            st.write(f"{shome.iloc[s, 1]}' {nome_fin} ({shome.iloc[s, 5][:1]})")
            with mat_tra1:
                if saway.shape[0]>0:
                    for s in list(range(saway.shape[0])):
                        nome_scor = saway.iloc[s, 0]
                        nome_split = nome_scor.split(' ')
                        nome_fin = '. '.join([x if x.isupper() else x[:1] for x in nome_split])
                        if (pd.notna(saway.iloc[s, 2])) & (pd.notna(saway.iloc[s, 3])):
                            st.write(
                                f"{saway.iloc[s, 1]}'+{saway.iloc[s, 2]} ({saway.iloc[s, 3]}) {nome_fin} ({saway.iloc[s, 5][:1]})")
                        elif (pd.notna(saway.iloc[s, 2])) & (pd.isna(saway.iloc[s, 3])):
                            st.write(
                                f"{saway.iloc[s, 1]}'+{saway.iloc[s, 2]} {nome_fin} ({saway.iloc[s, 5][:1]})")
                        elif (pd.isna(saway.iloc[s, 2])) & (pd.notna(saway.iloc[s, 3])):
                            st.write(
                                f"{saway.iloc[s, 1]}' ({saway.iloc[s, 3]}) {nome_fin} ({saway.iloc[s, 5][:1]})")
                        else:
                            st.write(f"{saway.iloc[s, 1]}' {nome_fin} ({saway.iloc[s, 5][:1]})")
    else:
        st.error('Partita non ancora giocata')

    with st.expander('Big Match'):
        st.markdown("*Com'è finito il doppio confronto stagionale tra prima e seconda classificata?*")
        bmcol, bmcol2 = st.columns(2)
        primo = classifica.iloc[0, 2]
        secondo = classifica.iloc[1, 2]
        search_bm = df[
            ((df['CASA'] == primo) & (df['TRAS'] == secondo)) | ((df['CASA'] == secondo) & (df['TRAS'] == primo))]
        search_bm = search_bm.sort_values('Giornata')
        search_bm.reset_index(drop=True, inplace=True)
        with bmcol:
            if search_bm.shape[0]>=1:
                and_bm = search_bm.iloc[0,:]
                st.write('Andata')
                st.write(f"Data: {and_bm['Giorno']}")
                acol1, acol2 = st.columns(2)
                with acol1:
                    st.image(Image.open(BytesIO(requests.get(load_images(team=and_bm['CASA'], yyyy=sea_sel)).content)))
                    st.write(f"{and_bm['CASA']}")
                    st.subheader(f"{and_bm['GC']}")
                with acol2:
                    st.image(Image.open(BytesIO(requests.get(load_images(team=and_bm['TRAS'], yyyy=sea_sel)).content)))
                    st.write(f"{and_bm['TRAS']}")
                    st.subheader(f"{and_bm['GT']}")
            else:
                st.error('Andata non ancora giocata')
        with bmcol2:
            if search_bm.shape[0] == 2:
                rit_bm = search_bm.iloc[1,:]
                st.write('Ritorno')
                st.write(f"Data: {rit_bm['Giorno']}")
                rcol1, rcol2 = st.columns(2)
                with rcol1:
                    st.image(Image.open(BytesIO(requests.get(load_images(team=rit_bm['CASA'], yyyy=sea_sel)).content)))
                    st.write(f"{rit_bm['CASA']}")
                    st.subheader(f"{rit_bm['GC']}")
                with rcol2:
                    st.image(Image.open(BytesIO(requests.get(load_images(team=rit_bm['TRAS'], yyyy=sea_sel)).content)))
                    st.write(f"{rit_bm['TRAS']}")
                    st.subheader(f"{rit_bm['GT']}")
            else:
                st.error('Ritorno non ancora giocato')
