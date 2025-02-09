import streamlit

from Funzioni import *
st.header('Le stagioni')

sea_sel=st.selectbox('Seleziona una stagione',seas_list)

df=storico[storico['Stagione']==sea_sel]
start_sea=min(df['Data'])
end_sea=max(df['Data'])
n_gio=max(df['Giornata'])

rc, ins = st.tabs(['Risultati e classifica','Insights'])
with rc:
    class_c, ris_c = st.columns([2, 1])
    with class_c:
        sel_date = st.slider("Seleziona il range di date:", min_value=start_sea, max_value=end_sea,value=(start_sea,end_sea),step=timedelta(days=1),format="DD/MM/YYYY")
        classifica=ranking(seas=sea_sel,st_date=sel_date[0],en_date=sel_date[1])
        stem = []
        for s in classifica['Squadra']:
            stem.append(load_images(team=s, yyyy=sea_sel[:4]))
        classifica.insert(1,"Badge",stem)
        st.dataframe(classifica,column_config={"Badge":st.column_config.ImageColumn()},hide_index=True)
    with ris_c:
        sel_gio = st.slider("Seleziona la giornata:",1,n_gio,n_gio)
        df['Giorno'] = pd.to_datetime(df['Data']).dt.strftime('%b %d, %Y')
        df['Risultato']=[str(x)+'-'+str(y) for x,y in zip(df['GC'],df['GT'])]
        df_fil_gio=df[df['Giornata']==sel_gio]
        st.dataframe(df_fil_gio[['Giorno','CASA','TRAS','Risultato']],hide_index=True)

    with st.expander('Andamento classifica'):
        c_cum=class_cum(seas=sea_sel)
        cum_gr = px.line(c_cum, x="Giornata", y="CumP", color="Squadra",markers=True)
        cum_gr.update_layout(xaxis_title="Giornata", yaxis_title="Punti Cumulati")
        st.plotly_chart(cum_gr)

    with st.expander('Classifica casa/trasferta'):
        clh, cla = st.columns(2)
        with clh:
            st.write('Classifica in casa:')
            st.dataframe(class_ct(seas=sea_sel)[0],hide_index=True)
        with cla:
            st.write('Classifica in trasferta:')
            st.dataframe(class_ct(seas=sea_sel)[1],hide_index=True)
#2 tab (1 ris e classifica, 2 insights su partite e gol, distribuzione gol ecc)

with ins:
    m1, m2, m3 = st.columns(3)