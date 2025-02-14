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

    colgc1, colgc2, colgc3 = st.columns(3)
    df1 = prec(t1=t1, t2=t2)
    df2 = prec(t1=t2, t2=t1)
    with colgc1:
        st.text(f'{t1} home')
        gauge1 = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=df1['Bil'].item(),
            mode="gauge+number",
            title={'text': "Bilancio"},
            gauge={'axis': {'range': [df1['TRAS'].item(), -df1['TRAS'].item()]},
                   'steps': [
                       {'range': [0,-df1['TRAS'].item()], 'color': "orange"},
                       {'range': [df1['TRAS'].item(),0], 'color': "blue"}]
                   }))
        st.plotly_chart(gauge1, use_container_width=True)
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            wh_d_wa1 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df1['WH'].item(), df1['N'].item() ,df1['WA'].item()],
                             labels=[f"W {t1}", "Pari", f"W {t2}"])
            st.plotly_chart(go.FigureWidget(data=wh_d_wa1), use_container_width=True)
        with subcol2:
            goal1 = go.Pie(hole=0.5, sort=False, direction='clockwise',
                              values=[df1['GC'].item(), df1['GT'].item() ],
                              labels=[f"Gol {t1}", "Pari", f"Gol {t2}"])
            st.plotly_chart(go.FigureWidget(data=goal1), use_container_width=True)
    with colgc3:
        st.text(f'{t2} home')
        gauge3 = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=df2['Bil'].item(),
            mode="gauge+number",
            title={'text': "Bilancio"},
            gauge={'axis': {'range': [-df2['TRAS'].item(), df2['TRAS'].item()]},
                   'steps': [
                       {'range': [-df2['TRAS'].item(),0], 'color': "orange"},
                       {'range': [0,df2['TRAS'].item()], 'color': "blue"}]
                   }))
        st.plotly_chart(gauge3, use_container_width=True)
        subcol3, subcol4 = st.columns(2)
        with subcol3:
            wh_d_wa2 = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[df2['WH'].item(), df2['N'].item() ,df2['WA'].item()],
                             labels=[f"W {t2}", "Pari", f"W {t1}"])
            st.plotly_chart(go.FigureWidget(data=wh_d_wa2), use_container_width=True)
        with subcol4:
            goal2 = go.Pie(hole=0.5, sort=False, direction='clockwise',
                              values=[df2['GC'].item(), df2['GT'].item() ],
                              labels=[f"Gol {t2}", "Pari", f"Gol {t1}"])
            st.plotly_chart(go.FigureWidget(data=goal2), use_container_width=True)
