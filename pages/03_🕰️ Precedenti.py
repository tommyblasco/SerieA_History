import streamlit as st
st.set_page_config(page_title="Serie A - Precedenti",layout='wide')

from Funzioni import *

st.title("Precedenti")

h2h, riep = st.tabs(['Testa a testa','Riepilogo x squadra'])

with h2h:
    colt1, colt2 = st.columns(2)
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

        with colgc1:
            st.text(f'{t1} home')
            m1, m2 = st.columns(2)
            m1.metric(label='Partite giocate',value=df1['TRAS'].item())
            m2.metric(label='Bilancio POV Home', value=df1['WH'].item()-df1['WA'].item(),border=True)

            wh_d_wa1 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df1['WH'].item(), df1['N'].item() ,df1['WA'].item()],
                                 labels=[f"W {t1}", "Pari", f"W {t2}"])
            st.plotly_chart(go.FigureWidget(data=wh_d_wa1), use_container_width=True)

            m3, m4 = st.columns(2)
            m3.metric(label=f'Gol fatti {t1}',value=df1['GC'].item())
            m4.metric(label=f'Gol fatti {t2}', value=df1['GT'].item())
        with colgc2:
            st.text("COMPLESSIVO")
            st.metric(label='Partite giocate in serie A', value=df1['TRAS'].item()+df2['TRAS'].item())

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[0], y=[-0.1], mode="markers", marker=dict(symbol="triangle-up", size=50, color="yellow")))
            beta=((df1['WH'].item()+df2['WA'].item())/(df2['WH'].item()+df1['WA'].item()))-1
            fig.add_trace(go.Scatter(x=[-2,0,2], y= np.asarray([-2,0,2])*beta, showlegend=False))
            fig.add_trace(go.Scatter(x=[-2,2], y=[(-2*beta)+0.1, (2*beta)+0.1], mode='markers',
                                     marker=dict(color=['orange','blue'],size=[df1['WH'].item()+df2['WA'].item(),df2['WH'].item()+df1['WA'].item()])))
            fig.update_layout(xaxis=dict(showgrid=False,showticklabels=False), yaxis=dict(range=[-2,2],showgrid=False,showticklabels=False))

            st.plotly_chart(fig, use_container_width=True)

            wh_d_wa3 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df1['WH'].item()+df2['WA'].item(), df1['N'].item()+df2['N'].item() ,df1['WA'].item()+df2['WH'].item()],
                                 labels=[f"W {t1}", "Pari", f"W {t2}"])
            st.plotly_chart(go.FigureWidget(data=wh_d_wa3), use_container_width=True)
        with colgc3:
            st.text(f'{t2} home')
            m5, m6 = st.columns(2)
            m5.metric(label='Partite giocate',value=df2['TRAS'].item())
            m6.metric(label='Bilancio POV Home', value=df2['WH'].item()-df2['WA'].item(),border=True)

            wh_d_wa2 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df2['WH'].item(), df2['N'].item() ,df2['WA'].item()],
                                 labels=[f"W {t2}", "Pari", f"W {t1}"])
            st.plotly_chart(go.FigureWidget(data=wh_d_wa2), use_container_width=True)
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