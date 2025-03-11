#st.set_page_config(page_title="Serie A - Precedenti",layout='wide')
from Funzioni import *

storico=get_storico()
marcatori=get_marcatori()
lista_sq=sorted(set(list(storico['CASA'])+list(storico['TRAS'])))
lista_mr=sorted(set(list(storico['All CASA'])+list(storico['All TRAS'])))

st.title("Precedenti")

h2h, h2hmr, riep = st.tabs(['Testa a testa','H2H allenatori-team','Riepilogo x squadra'])

with h2h:
    st.markdown("*Chi ha vinto di più in serie A tra le 2 squadre?*")
    colt1, colt2 = st.columns(2)
    with colt1:
        t1=st.selectbox('Seleziona il team 1:',lista_sq)
    with colt2:
        lsq2 = [x for x in lista_sq if x != t1]
        t2=st.selectbox('Seleziona il team 2:',lsq2)
    df1 = prec(dati=storico,t1=t1, t2=t2)[0]
    df2 = prec(dati=storico,t1=t1, t2=t2)[1]
    if (df1.shape[0]==0) | (df2.shape[0]==0):
        st.error('Nessun precedente trovato')
    else:
        wt1=df1['WH'].item()+df2['WA'].item()
        wt2=df2['WH'].item()+df1['WA'].item()
        n_gio=df1['TRAS'].item()+df2['TRAS'].item()
        pareg=df1['N'].item() + df2['N'].item()

        pretot1, pretot2 = st.columns([1,5])
        with pretot1:
            st.metric(label='Tot precedenti in serie A', value=n_gio)
        with pretot2:
            logo1 = base64.b64encode(BytesIO(requests.get(load_images(team=t1, yyyy='2999')).content).read()).decode()
            logo2 = base64.b64encode(BytesIO(requests.get(load_images(team=t2, yyyy='2999')).content).read()).decode()
            colr1 = colori_team.loc[colori_team['Squadra'] == t1, 'Colore'].item()
            colr2 = colori_team.loc[colori_team['Squadra'] == t2, 'Colore'].item()
            tab_prec = go.Figure(
                layout=go.Layout(
                    xaxis=dict(range=[0, 2], showgrid=False, zeroline=False, visible=False),
                    yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
                    plot_bgcolor='black', showlegend=False,
                    shapes=[
                        dict(type="rect", x0=0, y0=0, x1=0.8, y1=1,
                             line=dict(width=2, color='white'), fillcolor=colr1, layer="below"),
                        dict(type="rect", x0=1.2, y0=0, x1=2, y1=1,
                             line=dict(width=2, color='white'), fillcolor=colr2, layer="below"),
                        dict(type="rect", x0=0.8, y0=0, x1=1.2, y1=1,
                             line=dict(width=2, color='white'), fillcolor='rgb(86, 86, 86)', layer="below"),
                    ]
                    , images=[
                        dict(source=f'data:image/png;base64,{logo1}', x=0.05, y=0.5, xref="x", yref="y",
                             sizex=0.2, sizey=0.4, xanchor="left", yanchor="middle"),
                        dict(source=f'data:image/png;base64,{logo2}', x=1.95, y=0.5, xref="x", yref="y",
                             sizex=0.2, sizey=0.4, xanchor="right", yanchor="middle"),
                    ]
                )
            )
            tab_prec.add_trace(go.Scatter(x=[0.9], y=[0.5], text=str(wt1), mode="text",
                                           textfont=dict(size=30, color='white', family='Arial Black')))

            tab_prec.add_trace(go.Scatter(x=[0.4], y=[0.5], text=t1, mode="text",
                                           textfont=dict(size=15, color='white', family='Arial Black')))

            tab_prec.add_trace(go.Scatter(x=[1.1], y=[0.5], text=str(wt2), mode="text",
                                           textfont=dict(size=30, color='white', family='Arial Black')))

            tab_prec.add_trace(go.Scatter(x=[1.5], y=[0.5], text=t2, mode="text",
                                           textfont=dict(size=15, color='white', family='Arial Black'),
                                           textposition="middle right"))
            tab_prec.add_trace(go.Scatter(x=[0.98], y=[0.5], text=str(pareg), mode="text",
                                          textfont=dict(size=30, color='white', family='Arial Black')))
            tab_prec.add_trace(go.Scatter(x=[0.95], y=[0.85], text='Pareggi', mode="text",
                                          textfont=dict(size=15, color='white', family='Arial Black')))
            st.plotly_chart(tab_prec)

        colgc1, colgc3 = st.columns(2)
        with colgc1:
            st.text(f'{t1} home')
            wh_d_wa1 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df1['WH'].item(), df1['N'].item() ,df1['WA'].item()],
                                 labels=[f"W {t1}", "Pari", f"W {t2}"], marker=dict(colors=['orange','grey','blue']))
            st.plotly_chart(go.FigureWidget(data=wh_d_wa1), use_container_width=True)
            m1, m2 = st.columns(2)
            m1.metric(label='Partite giocate',value=df1['TRAS'].item())
            m2.metric(label='Bilancio POV Home', value=df1['WH'].item()-df1['WA'].item(),border=True)
            m3, m4 = st.columns(2)
            m3.metric(label=f'Gol fatti {t1}',value=df1['GC'].item())
            m4.metric(label=f'Gol fatti {t2}', value=df1['GT'].item())

        with colgc3:
            st.text(f'{t2} home')
            wh_d_wa2 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df2['WH'].item(), df2['N'].item() ,df2['WA'].item()],
                                 labels=[f"W {t2}", "Pari", f"W {t1}"],marker=dict(colors=['blue','grey','orange']))
            st.plotly_chart(go.FigureWidget(data=wh_d_wa2), use_container_width=True)
            m5, m6 = st.columns(2)
            m5.metric(label='Partite giocate',value=df2['TRAS'].item())
            m6.metric(label='Bilancio POV Home', value=df2['WH'].item()-df2['WA'].item(),border=True)
            m7, m8 = st.columns(2)
            m7.metric(label=f'Gol fatti {t2}', value=df2['GC'].item())
            m8.metric(label=f'Gol fatti {t1}', value=df2['GT'].item())

        st.subheader('Andamento precedenti nel tempo')
        st.markdown("*Chi era solito vincere nel passato tra i 2 team?*")
        pre_cum = prec(dati=storico,t1=t1, t2=t2)[2]
        cump_gr = px.area(pre_cum, x="Stagione", y="CumPr", markers=True)
        cump_gr.update_layout(xaxis=dict(title="Stagione", type="category"))
        cump_gr.add_annotation( x=-0.2, y=max(pre_cum["CumPr"]),showarrow=False,
            text=f"{t1}", yref="y")
        cump_gr.add_annotation(x=-0.2, y=min(pre_cum["CumPr"]), showarrow=False,
                               text=f"{t2}", yref="y")
        st.plotly_chart(cump_gr)

    with st.expander('Dettaglio partite'):
        st.markdown("*Scopri tutti i risultati dei precedenti tra i 2 team*")
        detcol1, detcol2, detcol3 = st.columns(3)
        with detcol1:
            dft1 = storico[(storico['CASA']==t1) & (storico['TRAS']==t2)].sort_values('Data',ascending=False)
            dft1.reset_index(drop=True, inplace=True)
            dft1['Risultato'] = [str(x) + '-' + str(y) for x, y in zip(dft1['GC'], dft1['GT'])]
            st.dataframe(dft1[['CASA','TRAS','Risultato','Stagione','Giorno']], hide_index=True)
        with detcol3:
            dft2 = storico[(storico['CASA']==t2) & (storico['TRAS']==t1)].sort_values('Data',ascending=False)
            dft2.reset_index(drop=True, inplace=True)
            dft2['Risultato'] = [str(x) + '-' + str(y) for x, y in zip(dft2['GC'], dft2['GT'])]
            st.dataframe(dft2[['CASA','TRAS','Risultato','Stagione','Giorno']], hide_index=True)
        with detcol2:
            dftot = pd.concat([dft1,dft2],ignore_index=True).sort_values('Data',ascending=False)
            dftot.reset_index(drop=True, inplace=True)
            dftot['Risultato'] = [str(x) + '-' + str(y) for x, y in zip(dftot['GC'], dftot['GT'])]
            st.dataframe(dftot[['CASA','TRAS','Risultato','Stagione','Giorno']], hide_index=True)

    with st.expander('I mattatori della sfida'):
        st.markdown("*Chi è stato il bomber della sfida tra i 2 team in serie A?*")
        dfglob=storico[((storico['CASA']==t1) & (storico['TRAS']==t2)) | ((storico['CASA']==t2) & (storico['TRAS']==t1))]
        ids_m = [x for x in dfglob['ID']]
        marcatori_prec = marcatori[marcatori['ID'].isin(ids_m)]
        marcatori_prec = marcatori_prec[(marcatori_prec['Note']!='A') | pd.isna(marcatori_prec['Note'])]
        marcatori_prec['t1']=[1 if x==t1 else 0 for x in marcatori_prec['Squadra']]
        marcatori_prec['t2']=[1 if x==t2 else 0 for x in marcatori_prec['Squadra']]
        mtot=marcatori_prec.groupby('Marcatori',as_index=False).agg({'t1':'sum','t2':'sum'})
        mtot['Tot Gol']=[x+y for x,y in zip(mtot['t1'],mtot['t2'])]
        mtot=mtot.sort_values('Tot Gol',ascending=False)
        mtot.columns=['Bombers',f'Per {t1}',f'per {t2}','Totale']
        st.dataframe(mtot,hide_index=True)

    with st.expander('Record'):
        st.markdown("*Da quanto tempo una squadra non vince in casa dell'altra?*")
        reccol1, reccol2 = st.columns(2)
        with reccol1:
            wte1h = dft1[dft1['GC']>dft1['GT']]
            if wte1h.shape[0]>0:
                ggwte1h=wte1h['Data'].iloc[0]
                st.write(f"Ultima vittoria {t1} in casa:")
                st.write(f"{t1}-{t2} {wte1h['GC'].iloc[0]}-{wte1h['GT'].iloc[0]}")
                st.write(f"il {wte1h['Giorno'].iloc[0]}, {(date.today()-ggwte1h).days} giorni fa")
            else:
                st.warning(f'Nessuna vittoria in casa per {t1}')
            st.divider()
            lte1h = dft1[dft1['GC'] < dft1['GT']]
            if lte1h.shape[0]>0:
                gglte1h = lte1h['Data'].iloc[0]
                st.write(f"Ultima vittoria {t2} in trasferta:")
                st.write(f"{t1}-{t2} {lte1h['GC'].iloc[0]}-{lte1h['GT'].iloc[0]}")
                st.write(f"il {lte1h['Giorno'].iloc[0]}, {(date.today() - gglte1h).days} giorni fa")
            else:
                st.warning(f'Nessuna vittoria in trasferta per {t2}')
        with reccol2:
            wte2h = dft2[dft2['GC'] > dft2['GT']]
            if wte2h.shape[0]>0:
                ggwte2h = wte2h['Data'].iloc[0]
                st.write(f"Ultima vittoria {t2} in casa:")
                st.write(f"{t2}-{t1} {wte2h['GC'].iloc[0]}-{wte2h['GT'].iloc[0]}")
                st.write(f"il {wte2h['Giorno'].iloc[0]}, {(date.today() - ggwte2h).days} giorni fa")
            else:
                st.warning(f'Nessuna vittoria in casa per {t2}')
            st.divider()
            lte2h = dft2[dft2['GC'] < dft2['GT']]
            if lte2h.shape[0]>0:
                gglte2h = lte2h['Data'].iloc[0]
                st.write(f"Ultima vittoria {t1} in trasferta:")
                st.write(f"{t2}-{t1} {lte2h['GC'].iloc[0]}-{lte2h['GT'].iloc[0]}")
                st.write(f"il {lte2h['Giorno'].iloc[0]}, {(date.today() - gglte2h).days} giorni fa")
            else:
                st.warning(f'Nessuna vittoria in trasferta per {t1}')

with h2hmr:
    st.markdown("*Chi ha vinto di più in serie A tra 2 mister o tra un mister e una squadra?*")
    conf=st.pills("Scegli un confronto",['Mr vs Mr','Mr vs Team'])
    colmr, colmr2 = st.columns(2)
    if conf=="Mr vs Mr":
        with colmr:
            mr1 = st.selectbox('Seleziona il mister 1:', lista_mr)
            mr_avail=[x if y==mr1 else y if x==mr1 else '' for x,y in zip(storico['All CASA'],storico['All TRAS'])]
            mr_avail_fin=sorted(set([x for x in mr_avail if x!='']))
        with colmr2:
            mr2 = st.selectbox('Seleziona il mister 2:', mr_avail_fin)
        mrgr1, mrgr2 = st.columns(2)
        prec_mrs=prec_with_mr(dati=storico, type="MM", i1=mr1, i2=mr2)
        with mrgr1:
            st.metric(label='Precedenti in A',value=prec_mrs[0])
            met1, met2, met3 = st.columns(3)
            met1.metric(label=f"Vittorie {mr1}",value=prec_mrs[1])
            met2.metric(label="Pareggi", value=prec_mrs[2])
            met3.metric(label=f"Vittorie {mr2}", value=prec_mrs[3])
        with mrgr2:
            wh_d_wa_mrs = go.Pie(hole=0.5, sort=False, direction='clockwise',
                              values=[prec_mrs[1], prec_mrs[2], prec_mrs[3]],
                              labels=[f"W {mr1}", "Pari", f"W {mr2}"], marker=dict(colors=['orange', 'grey', 'blue']))
            st.plotly_chart(go.FigureWidget(data=wh_d_wa_mrs), use_container_width=True)
        st.divider()

        st.subheader('Dettaglio partite')
        dfmr = storico[((storico['All CASA'] == mr1) & (storico['All TRAS'] == mr2))|((storico['All CASA']==mr2) & (storico['All TRAS']==mr1))].sort_values('Data',ascending=False)
        dfmr.reset_index(drop=True, inplace=True)
        dfmr['Risultato'] = [str(x) + '-' + str(y) for x, y in zip(dfmr['GC'], dfmr['GT'])]
        st.dataframe(dfmr[['All CASA','All TRAS','CASA', 'TRAS', 'Risultato', 'Stagione', 'Giorno']], hide_index=True)

        with st.expander('Riepilogo allenatore vs allenatore'):
            mrfin = st.selectbox('Seleziona un mister:', lista_mr)
            df_mrfin = riepilogo_prec(dati=storico, type='MM', i1=mrfin)
            hbarmm = go.Figure()
            hbarmm.add_trace(go.Bar(x=df_mrfin['W'], y=df_mrfin['Opponent'], orientation='h', marker=dict(color='green'),
                                   text=df_mrfin['W']))
            hbarmm.add_trace(go.Bar(x=df_mrfin['D'], y=df_mrfin['Opponent'], orientation='h', marker=dict(color='gray'),
                                   text=df_mrfin['D']))
            hbarmm.add_trace(go.Bar(x=df_mrfin['L'], y=df_mrfin['Opponent'], orientation='h', marker=dict(color='red'),
                                   text=df_mrfin['L']))
            hbarmm.update_layout(barmode='stack', showlegend=False, height=1600)
            hbarmm.update_traces(textangle=0)
            hbarmm.update_xaxes(side='top')
            st.plotly_chart(hbarmm)
    else:
        with colmr:
            mr1 = st.selectbox('Seleziona il mister:', lista_mr)
            t_avail = [y if x != mr1 else z if x == mr1 else '' for x, y, z in
                        zip(storico['All CASA'], storico['CASA'], storico['TRAS'])]
            t_avail_fin = sorted(set([x for x in t_avail if x != '']))
        with colmr2:
            tm1 = st.selectbox('Seleziona il team:', t_avail_fin)
        mrgr1, mrgr2 = st.columns(2)
        prec_mrs = prec_with_mr(dati=storico, type="MT", i1=mr1, i2=tm1)
        with mrgr1:
            st.metric(label='Precedenti in A', value=prec_mrs[0])
            met1, met2, met3 = st.columns(3)
            met1.metric(label=f"Vittorie {mr1}", value=prec_mrs[1])
            met2.metric(label="Pareggi", value=prec_mrs[2])
            met3.metric(label=f"Vittorie {tm1}", value=prec_mrs[3])
        with mrgr2:
            wh_d_wa_mrs = go.Pie(hole=0.5, sort=False, direction='clockwise',
                                 values=[prec_mrs[1], prec_mrs[2], prec_mrs[3]],
                                 labels=[f"W {mr1}", "Pari", f"W {tm1}"],
                                 marker=dict(colors=['orange', 'grey', 'blue']))
            st.plotly_chart(go.FigureWidget(data=wh_d_wa_mrs), use_container_width=True)
        st.divider()

        st.subheader('Dettaglio partite')
        dfmr = storico[((storico['All CASA'] == mr1) & (storico['TRAS'] == tm1)) | (
                    (storico['CASA'] == tm1) & (storico['All TRAS'] == mr1))].sort_values('Data', ascending=False)
        dfmr.reset_index(drop=True, inplace=True)
        dfmr['Risultato'] = [str(x) + '-' + str(y) for x, y in zip(dfmr['GC'], dfmr['GT'])]
        st.dataframe(dfmr[['All CASA', 'All TRAS', 'CASA', 'TRAS', 'Risultato', 'Stagione', 'Giorno']], hide_index=True)

        with st.expander('Riepilogo allenatore vs squadra'):
            mrfin = st.selectbox('Seleziona un mister:', lista_mr)
            df_mrfin = riepilogo_prec(dati=storico, type='MT', i1=mrfin)
            hbarmm = go.Figure()
            hbarmm.add_trace(
                go.Bar(x=df_mrfin['W'], y=df_mrfin['Opponent'], orientation='h', marker=dict(color='green'),
                       text=df_mrfin['W']))
            hbarmm.add_trace(go.Bar(x=df_mrfin['D'], y=df_mrfin['Opponent'], orientation='h', marker=dict(color='gray'),
                                    text=df_mrfin['D']))
            hbarmm.add_trace(go.Bar(x=df_mrfin['L'], y=df_mrfin['Opponent'], orientation='h', marker=dict(color='red'),
                                    text=df_mrfin['L']))
            hbarmm.update_layout(barmode='stack', showlegend=False, height=1600)
            hbarmm.update_traces(textangle=0)
            hbarmm.update_xaxes(side='top')
            st.plotly_chart(hbarmm)



with riep:
    tt1 = st.selectbox('Seleziona una squadra:', lista_sq)
    st.markdown("*Contro chi la squadra ha un bilancio tra vittorie e sconfitte più favorevole?*")
    df_tt1_g = riepilogo_prec(dati=storico,type='TT',i1=tt1)

    colgg1, colgg2 = st.columns([3, 1])
    with colgg1:
        st.subheader('Distribuzione precedenti')
        hbar2 = go.Figure()
        hbar2.add_trace(go.Bar(x=df_tt1_g['W'], y=df_tt1_g['Opponent'], orientation='h', marker=dict(color='green'), text=df_tt1_g['W']))
        hbar2.add_trace(go.Bar(x=df_tt1_g['D'], y=df_tt1_g['Opponent'], orientation='h', marker=dict(color='gray'), text=df_tt1_g['D']))
        hbar2.add_trace(go.Bar(x=df_tt1_g['L'], y=df_tt1_g['Opponent'], orientation='h', marker=dict(color='red'), text=df_tt1_g['L']))
        hbar2.update_layout(barmode='stack', showlegend=False, height=1600)
        hbar2.update_traces(textangle=0)
        hbar2.update_xaxes(side='top')
        st.plotly_chart(hbar2)
    with colgg2:
        st.subheader('Bilancio')
        bar3 = go.Figure()
        bar3.add_trace(go.Bar(y=df_tt1_g['Opponent'], x=df_tt1_g['Bil'], orientation='h', marker_color=np.where(df_tt1_g["Bil"]<0, 'red', 'green') ))
        bar3.update_layout(height=1600)
        bar3.update_xaxes(side='top')
        bar3.update_yaxes(side='right')
        st.plotly_chart(bar3)