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
    class_c, ris_c = st.columns([3, 1])
    with class_c:

        sel_date = st.slider("Seleziona il range di date:", min_value=start_sea.to_pydatetime().date(), max_value=end_sea.to_pydatetime().date(),value=(start_sea.to_pydatetime().date(),end_sea.to_pydatetime().date()),step=timedelta(days=1),format="DD/MM/YYYY")
        classifica=ranking(seas=sea_sel,st_date=sel_date[0],en_date=sel_date[1])
        stem = []
        for s in classifica['Squadra']:
            stem.append(load_images(team=s, yyyy=sea_sel[:4]))
        classifica.insert(1,"Stemmi",stem)
        st.dataframe(classifica,column_config={"Stemmi":st.column_config.ImageColumn()})
    with ris_c:
        sel_gio = st.slider("Seleziona la giornata:",1,n_gio,n_gio)
        df['Giorno'] = pd.to_datetime(df['Data']).dt.strftime('%b %d, %Y')
        df['Risultato']=[str(x)+'-'+str(y) for x,y in zip(df['GC'],df['GT'])]
        st.dataframe(df[['Giorno','CASA','TRAS','Risultato']])

#2 tab (1 ris e classifica, 2 insights su partite e gol, distribuzione gol ecc)
#2 colonne una prende il 70 (classifica con slider tempo) l'altra il 30 (sel giornata con partite)
#2 expander uno andamentale uno class casa e trasferta