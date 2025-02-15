import streamlit as st
st.set_page_config(page_title="Serie A",layout='wide')
from Funzioni import *



st.title("Serie A")

st.subheader("Database storico della Serie A a girone unico")

stagione_curr=str(seas_list[0])  #stagione corrente

rpl, part = st.columns(2)
with rpl:
    st.text('Partecipazioni Serie A')
    part_gr = go.Figure()
    part_gr.add_trace(go.Bar(y=riep_grp['Squadre'], x=riep_grp['Stagioni'],orientation='h'))
    part_gr.update_layout(height=1200)
    part_gr.update_xaxes(side='top')
    st.plotly_chart(go.FigureWidget(data=part_gr))

    st.divider()

    clas_rbc['Scudetti']=[int(x) for x in clas_rbc['Scudetti']]
    bcr=barplot(df=clas_rbc,item_column='Squadra',value_column='Scudetti',time_column='Anno')
    rbc = bcr.plot(time_label='Anno', value_label='Scudetti', title='Scudetti vinti', frame_duration=1000)
    st.plotly_chart(rbc)
with part:
    st.subheader('Albo d\'oro')
    for i in range(0, len(albo), 4):
        cols = st.columns(4)
        for j, (_, row) in enumerate(albo.iloc[i:i + 4].iterrows()):
            with cols[j]:
                st.image(Image.open(BytesIO(requests.get(row['url_Stemma']).content)), caption=f"{row['Vincitore']} ({row['Stagione']})", use_container_width=True)

