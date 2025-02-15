import streamlit as st
st.set_page_config(page_title="Serie A - Precedenti",layout='wide')

from Funzioni import *

st.title("Precedenti")

h2h, riep = st.tabs(['Testa a testa','Riepilogo x squadra'])

with h2h:
    colt1, colfake, colt2 = st.columns([3,4,3])
    with colt1:
        t1=st.selectbox('Seleziona il team 1:',lista_sq)
        st.image(Image.open(BytesIO(requests.get(load_images(team=t1, yyyy='2999')).content)))
    with colt2:
        lsq2 = [x for x in lista_sq if x != t1]
        t2=st.selectbox('Seleziona il team 2:',lsq2)
        st.image(Image.open(BytesIO(requests.get(load_images(team=t2, yyyy='2999')).content)))
    df1 = prec(t1=t1, t2=t2)[0]
    df2 = prec(t1=t1, t2=t2)[1]
    if (df1.shape[0]==0) | (df2.shape[0]==0):
        st.error('Nessun precedente trovato')
    else:
        colgc1, colgc2, colgc3 = st.columns([3,4,3])
        wt1=df1['WH'].item()+df2['WA'].item()
        wt2=df2['WH'].item()+df1['WA'].item()
        n_gio=df1['TRAS'].item()+df2['TRAS'].item()
        pareg=df1['N'].item() + df2['N'].item()
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
            st.metric(label='Partite giocate in serie A', value=n_gio)
            st.text('così ripartite:')
            hbar = go.Figure()
            for i,col in zip([wt1,pareg,wt2],['orange','gray','blue']):
                hbar.add_trace(go.Bar(x=[i],y=['Bil'],orientation='h',marker=dict(color=[col]),text=[str(round(100*i/n_gio,2))+'%'],textposition='auto',textfont=dict(size=16)))
            hbar.update_layout(barmode='stack',showlegend=False,yaxis=dict(showticklabels=False),bargap=0.7)
            st.plotly_chart(go.FigureWidget(data=hbar), use_container_width=True)
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
        pre_cum = prec(t1=t1, t2=t2)[2]
        cump_gr = px.area(pre_cum, x="Stagione", y="CumPr", markers=True)
        cump_gr.update_layout(xaxis=dict(title="Stagione", type="category"))
        cump_gr.add_annotation( x=-0.2, y=max(pre_cum["CumPr"]),showarrow=False,
            text=f"{t1}", yref="y")
        cump_gr.add_annotation(x=-0.2, y=min(pre_cum["CumPr"]), showarrow=False,
                               text=f"{t2}", yref="y")
        st.plotly_chart(cump_gr)

    with st.expander('Dettaglio partite'):
        detcol1, detcol2, detcol3 = st.columns(3)
        with detcol1:
            dft1 = storico[(storico['CASA']==t1) & (storico['TRAS']==t2)].sort_values('Data',ascending=False)
            dft1.reset_index(drop=True, inplace=True)
            dft1['Risultato'] = [str(x) + '-' + str(y) for x, y in zip(dft1['GC'], dft1['GT'])]
            st.dataframe(dft1[['Stagione','Giorno','CASA','TRAS','Risultato']], hide_index=True)
        with detcol3:
            dft2 = storico[(storico['CASA']==t2) & (storico['TRAS']==t1)].sort_values('Data',ascending=False)
            dft2.reset_index(drop=True, inplace=True)
            dft2['Risultato'] = [str(x) + '-' + str(y) for x, y in zip(dft2['GC'], dft2['GT'])]
            st.dataframe(dft2[['Stagione','Giorno','CASA','TRAS','Risultato']], hide_index=True)
        with detcol2:
            dftot = pd.concat([dft1,dft2],ignore_index=True).sort_values('Data',ascending=False)
            dftot.reset_index(drop=True, inplace=True)
            dftot['Risultato'] = [str(x) + '-' + str(y) for x, y in zip(dftot['GC'], dftot['GT'])]
            st.dataframe(dftot[['Stagione','Giorno','CASA','TRAS','Risultato']], hide_index=True)

    with st.expander('Record'):
        reccol1, reccol2 = st.columns(2)
        with reccol1:
            wte1h = dft1[dft1['GC']>dft1['GT']]
            ggwte1h=wte1h.loc[0, 'Data'][0]
            st.write(f"Ultima vittoria {t1} in casa:")
            st.write(f"{t1}-{t2} {wte1h.loc[0,'GC'].item()}-{wte1h.loc[0,'GT'].item()}")
            st.write(f"il {ggwte1h}, {(date.today()-ggwte1h).days} giorni fa")
            st.divider()
            lte1h = dft1[dft1['GC'] < dft1['GT']]
            gglte1h = lte1h.loc[0, 'Data'][0]
            st.write(f"Ultima vittoria {t2} in trasferta:")
            st.write(f"{t1}-{t2} {lte1h.loc[0, 'GC'].item()}-{lte1h.loc[0, 'GT'].item()}")
            st.write(f"il {gglte1h}, {(date.today() - gglte1h).days} giorni fa")
        with reccol2:
            wte2h = dft2[dft2['GC'] > dft2['GT']]
            ggwte2h = wte2h.loc[0, 'Data'][0]
            st.write(f"Ultima vittoria {t2} in casa:")
            st.write(f"{t2}-{t1} {wte2h.loc[0, 'GC'].item()}-{wte2h.loc[0, 'GT'].item()}")
            st.write(f"il {ggwte2h}, {(date.today() - ggwte2h).days} giorni fa")
            st.divider()
            lte2h = dft2[dft2['GC'] < dft2['GT']]
            gglte2h = lte2h.loc[0, 'Data'][0]
            st.write(f"Ultima vittoria {t1} in trasferta:")
            st.write(f"{t2}-{t1} {lte2h.loc[0, 'GC'].item()}-{lte2h.loc[0, 'GT'].item()}")
            st.write(f"il {gglte2h}, {(date.today() - gglte2h).days} giorni fa")