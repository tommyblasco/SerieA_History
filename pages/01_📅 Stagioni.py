import streamlit as st
st.set_page_config(page_title="Serie A - Stagioni",layout='wide')
from Funzioni import *


st.header('Le stagioni')

sea_sel=st.selectbox('Seleziona una stagione',seas_list)

df=storico[storico['Stagione']==sea_sel]
start_sea=min(df['Data'])
end_sea=max(df['Data'])
n_gio=max(df['Giornata'])

rc, ins, sm = st.tabs(['Risultati e classifica','Insights','Special matches'])
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
        df_pivot = df.pivot_table(index='clus_GC', columns='clus_GT', values='GC', aggfunc='count')
        df_freq = df_pivot*100/df.shape[0]
        res_gr = go.Figure(data=go.Heatmap( z=df_freq.values, x=df_freq.columns, y=df_freq.index,
            text=df_freq.round(1).astype(str) + '%', texttemplate="%{text}",
            colorscale="blues", showscale=True))
        res_gr.update_layout(xaxis=dict(title="Gol Tras", type="category"),yaxis=dict(title="Gol Casa", type="category"))
        res_gr.update_xaxes(side='top')
        st.plotly_chart(go.FigureWidget(data=res_gr), use_container_width=True)

    with st.expander('Andamento gol per giornata'):
        df['gol_match'] = [x + y for x, y in zip(df['GC'], df['GT'])]
        agg_gol_gio=df.groupby(['Giornata'],as_index=False).agg({'gol_match':'mean'})
        gol_gio_gr = px.line(agg_gol_gio, x="Giornata", y="gol_match", markers=True)
        gol_gio_gr.update_layout(xaxis_title="Giornata", yaxis_title="Media gol segnati")
        st.plotly_chart(gol_gio_gr)

with sm:
    st.subheader('Ricerca partita:')
    l1=sorted(list(classifica['Squadra']))
    hcol, acol, scol = st.columns(3)
    with hcol:
        ht=st.selectbox('Seleziona la squadra in casa',l1)
        st.image(Image.open(BytesIO(requests.get(load_images(team=ht, yyyy=sea_sel)).content)))
    with acol:
        l2=[x for x in l1 if x!=ht]
        at=st.selectbox('Seleziona la squadra in trasferta',l2)
        st.image(Image.open(BytesIO(requests.get(load_images(team=at, yyyy=sea_sel)).content)))
    search_match=df[(df['CASA']==ht) & (df['TRAS']==at)]
    with scol:
        if search_match.shape[0]>0:
            st.write(f"Data: {search_match['Giorno'].item()}")
            st.write(f"Giornata: {search_match['Giornata'].item()}")
            st.subheader(f"Risultato: {search_match['GC'].item()}-{search_match['GT'].item()}")
        else:
            st.error('Partita non ancora giocata')

    with st.expander('Big Match'):
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