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
    with m1:
        played = df.shape[0]
        st.metric(label='Partite giocate',value=played)
    with m2:
        gol_tot = sum(df['GC'])+sum(df['GT'])
        st.metric(label='Gol segnati',value=gol_tot)
    with m3:
        media_gol = round(gol_tot/played,2)
        st.metric(label='Media gol',value=media_gol)
    st.divider()
    pie1, pie2 = st.columns(2)
    with pie1:
        wh=df[df['GC']>df['GT']].shape[0]
        wa = df[df['GC'] < df['GT']].shape[0]
        wh_d_wa = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[wh, played-wh-wa, wa],
                        labels=["W Casa","Pari", "W Tras"])
        st.plotly_chart(go.FigureWidget(data=wh_d_wa), use_container_width=True)

        un_ov = st.slider("Seleziona la soglia U/O:", min_value=0.5, max_value=5.5, value=2.5)
        over = [x + y for x, y in zip(df['GC'], df['GT']) if x + y > un_ov]
        under = [x + y for x, y in zip(df['GC'], df['GT']) if x + y < un_ov]
        uo_gr = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[len(under), len(over)],
                       labels=["Under", "Over"])
        st.plotly_chart(go.FigureWidget(data=uo_gr), use_container_width=True)
    with pie2:
        gca=sum(df['GC'])
        gtr = sum(df['GT'])
        gct = go.Pie(hole=0.5, sort=False, direction='clockwise', values=[gca, gtr],
                        labels=["Gol Casa","Gol Tras"])
        st.plotly_chart(go.FigureWidget(data=gct), use_container_width=True)

        st.write('Distribuzione gol per match')
        n_gol = [x + y for x, y in zip(df['GC'], df['GT'])]
        dis_gol = go.Figure()
        dis_gol.add_trace(go.Histogram(x=n_gol, name="count"))
        st.plotly_chart(go.FigureWidget(data=dis_gol), use_container_width=True)

    with st.expander('Frequenza risultati'):
        df['clus_GC']=[str(x) if x<=4 else '>4' for x in df['GC']]
        df['clus_GT'] = [str(x) if x <= 4 else '>4' for x in df['GT']]
        df_pivot = df.pivot_table(index='clus_GC', columns='clus_GT', values='Squadra', aggfunc='count')
        df_freq = df_pivot/df.shape[0]
        res_gr = fig = px.imshow(df_freq, text_auto=True)
        st.plotly_chart(go.FigureWidget(data=res_gr), use_container_width=True, theme="streamlit")
