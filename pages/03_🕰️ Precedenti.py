#st.set_page_config(page_title="Serie A - Precedenti",layout='wide')
from Funzioni import *

storico=get_storico()
marcatori=get_marcatori()
lista_sq=sorted(set(list(storico['CASA'])+list(storico['TRAS'])))


st.title("Precedenti")

h2h, riep = st.tabs(['Testa a testa','Riepilogo x squadra'])

with h2h:
    st.markdown("*Chi ha vinto di più in serie A tra le 2 squadre?*")
    colt1, colfake, colt2 = st.columns([3,4,3])
    with colt1:
        t1=st.selectbox('Seleziona il team 1:',lista_sq)
        st.image(Image.open(BytesIO(requests.get(load_images(team=t1, yyyy='2999')).content)))
    with colt2:
        lsq2 = [x for x in lista_sq if x != t1]
        t2=st.selectbox('Seleziona il team 2:',lsq2)
        st.image(Image.open(BytesIO(requests.get(load_images(team=t2, yyyy='2999')).content)))
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
            st.metric(label='Partite giocate in serie A', value=n_gio)
        with pretot2:
            hbar = go.Figure()
            for i, col in zip([wt1, pareg, wt2], ['orange', 'gray', 'blue']):
                hbar.add_trace(go.Bar(x=[i], y=['Bil'], orientation='h', marker=dict(color=[col]),
                                      text=[str(round(100 * i / n_gio, 2)) + '%'], textposition='auto',
                                      textfont=dict(size=16)))
            hbar.update_layout(barmode='stack', showlegend=False, yaxis=dict(showticklabels=False), margin=dict(l=0,r=0,t=0,b=0),height=100)
            st.plotly_chart(go.FigureWidget(data=hbar), use_container_width=True)

        colgc1, colgc2, colgc3 = st.columns([3,4,3])
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
        with colgc2:
            st.subheader("      COMPLESSIVO")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[0], y=[-0.1], mode="markers", marker=dict(symbol="triangle-up", size=50, color="yellow"), showlegend=False))
            beta=(wt1/wt2)-1
            fig.add_trace(go.Scatter(x=[-2,0,2], y= np.asarray([-2,0,2])*beta, showlegend=False))
            fig.add_trace(go.Scatter(x=[-2,2], y=[(-2*beta)+0.1, (2*beta)+0.1], mode='markers', showlegend=False,
                                     marker=dict(color=['orange','blue'],size=[wt1,wt2],sizemode='area',sizeref=2.*max(wt1,wt2)/(70.**2))))
            fig.update_layout(xaxis=dict(showgrid=False,showticklabels=False), yaxis=dict(range=[-2,2],showgrid=False,showticklabels=False))
            fig.add_annotation(x=-1.9, y=(-2 * beta) + 0.7, showarrow=False,
                               text=f"{wt1}",font=dict(size=25))
            fig.add_annotation(x=-1.9, y=(-2*beta)+0.4, showarrow=False, text=f"W {t1}")
            fig.add_annotation(x=1.9, y=(2 * beta) + 0.7, showarrow=False,
                               text=f"{wt2}",font=dict(size=25))
            fig.add_annotation(x=1.9, y=(2 * beta) + 0.4, showarrow=False,text=f"W {t2}")
            fig.add_annotation(x=0, y=0.4, showarrow=False, text=f"{pareg} pareggi")
            st.plotly_chart(fig, use_container_width=True)

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

with riep:
    tt1 = st.selectbox('Seleziona una squadra:', lista_sq)
    st.markdown("*Contro chi la squadra ha un bilancio tra vittorie e sconfitte più favorevole?*")
    df_tt1 = storico[(storico['CASA'] == tt1) | (storico['TRAS'] == tt1)]
    df_tt1['Opponent']=[x if x!=tt1 else y for x,y in zip(df_tt1['CASA'],df_tt1['TRAS'])]
    df_tt1['W']=[1 if ((x==tt1) & (y>z) | (x!=tt1) & (z>y)) else 0 for x,y,z in zip(df_tt1['CASA'],df_tt1['GC'],df_tt1['GT'])]
    df_tt1['D'] =[1 if x==y else 0 for x,y in zip(df_tt1['GC'],df_tt1['GT'])]
    df_tt1['L']=[1 if ((x==tt1) & (y<z) | (x!=tt1) & (z<y)) else 0 for x,y,z in zip(df_tt1['CASA'],df_tt1['GC'],df_tt1['GT'])]
    df_tt1_g=df_tt1.groupby('Opponent',as_index=False).agg({'CASA':'count','W':'sum','D':'sum','L':'sum'}).sort_values(['CASA','W'])
    df_tt1_g['Bil']=[x-y for x,y in zip(df_tt1_g['W'],df_tt1_g['L'])]
    df_tt1_g.reset_index(drop=True, inplace=True)

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