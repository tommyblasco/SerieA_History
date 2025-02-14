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
            st.metric(label='Partite giocate',value=df1['TRAS'].item())
            gauge1 = go.Figure(go.Indicator(
                domain={'x': [0, 1], 'y': [0, 1]},
                value=int(df1['Bil'].item()),
                mode="gauge+number",
                title={'text': "Bilancio"},
                gauge={'axis': {'range': [df1['TRAS'].item(), -df1['TRAS'].item()]},
                       'steps': [
                           {'range': [0,-df1['TRAS'].item()], 'color': "orange"},
                           {'range': [df1['TRAS'].item(),0], 'color': "blue"}]
                       }))
            st.plotly_chart(gauge1, use_container_width=True)

            wh_d_wa1 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df1['WH'].item(), df1['N'].item() ,df1['WA'].item()],
                                 labels=[f"W {t1}", "Pari", f"W {t2}"])
            st.plotly_chart(go.FigureWidget(data=wh_d_wa1), use_container_width=True)
        with colgc2:
            st.text("COMPLESSIVO")
            st.metric(label='Partite giocate in serie A', value=df1['TRAS'].item()+df2['TRAS'].item())
            gauge2 = go.Figure(go.Indicator(
                domain={'x': [0, 1], 'y': [0, 1]},
                value=int(df1['Bil'].item())-int(df2['Bil'].item()),
                mode="gauge+number",
                title={'text': "Bilancio"},
                gauge={'axis': {'range': [df1['TRAS'].item()+df2['TRAS'].item(), -df1['TRAS'].item()-df2['TRAS'].item()]},
                       'steps': [
                           {'range': [0,-df1['TRAS'].item()-df2['TRAS'].item()], 'color': "orange"},
                           {'range': [df1['TRAS'].item()+df2['TRAS'].item(),0], 'color': "blue"}]
                       }))
            st.plotly_chart(gauge2, use_container_width=True)

            wh_d_wa3 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df1['WH'].item()+df2['WA'].item(), df1['N'].item()+df2['N'].item() ,df1['WA'].item()+df2['WH'].item()],
                                 labels=[f"W {t1}", "Pari", f"W {t2}"])
            st.plotly_chart(go.FigureWidget(data=wh_d_wa3), use_container_width=True)
        with colgc3:
            st.text(f'{t2} home')
            st.metric(label='Partite giocate', value=df2['TRAS'].item())
            gauge3 = go.Figure(go.Indicator(
                domain={'x': [0, 1], 'y': [0, 1]},
                value=-df2['Bil'].item(),
                mode="gauge+number",
                title={'text': "Bilancio"},
                gauge={'axis': {'range': [-df2['TRAS'].item(), df2['TRAS'].item()]},
                       'steps': [
                           {'range': [df2['TRAS'].item(),0], 'color': "blue"},
                           {'range': [0,-df2['TRAS'].item()], 'color': "orange"}]
                       }))
            st.plotly_chart(gauge3, use_container_width=True)
            wh_d_wa2 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df2['WA'].item(), df2['N'].item() ,df2['WH'].item()],
                                 labels=[f"W {t1}", "Pari", f"W {t2}"])
            st.plotly_chart(go.FigureWidget(data=wh_d_wa2), use_container_width=True)
        st.subheader('Andamento precedenti nel tempo')
        pre_cum = prec(t1=t1, t2=t2)[2]
        cump_gr = px.area(pre_cum, x="Stagione", y="CumPr", markers=True)
        cump_gr.update_layout(xaxis=dict(title="Stagione", type="category"))
        cump_gr.add_annotation( x=-0.2, y=max(pre_cum["CumPr"]),showarrow=False,
            text=f"{t1}", yref="y")
        cump_gr.add_annotation(x=-0.2, y=min(pre_cum["CumPr"]), showarrow=False,
                               text=f"{t2}", yref="y")
        st.plotly_chart(cump_gr)