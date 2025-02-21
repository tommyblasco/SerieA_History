import streamlit as st
st.set_page_config(page_title="Serie A - All time",layout='wide')
from Funzioni import *

perp, rec = st.tabs(['Classifica perpetua','Record'])

with perp:
    st.subheader('Classifica perpetua')
    st.markdown("*Quale squadra ha la maggiore media punti in Serie A?*")
    pclass=ranking(seas='All').drop('Rk',axis=1)
    st.dataframe(pclass, hide_index=True)

    with st.expander('Media gol stagionale'):
        st.markdown("*E' vero che negli anni 70 e 80 si segnava di meno?*")
        storico['Gol Tot']=[x+y for x,y in zip(storico['GC'],storico['GT'])]
        dfg=storico.groupby('Stagione',as_index=False).agg({'Gol Tot':'mean'})
        df_gr = px.line(dfg, x="Stagione", y="Gol Tot", markers=True)
        df_gr.update_layout(xaxis=dict(title="Stagione", type="category"),yaxis=dict(title="Media Gol"))
        st.plotly_chart(df_gr)
    with st.expander('Vittorie C/T stagionale'):
        st.markdown("*Com'è cambiato il fattore campo stagione dopo stagione?*")
        storico['WH']=[100 if x>y else 0 for x,y in zip(storico['GC'],storico['GT'])]
        storico['WA'] = [100 if x < y else 0 for x, y in zip(storico['GC'], storico['GT'])]
        storico['N'] = [100 if x == y else 0 for x, y in zip(storico['GC'], storico['GT'])]
        dfg1 = storico.groupby('Stagione', as_index=False).agg({'WH': 'mean','WA':'mean','N':'mean'})
        dfg1_gr = px.bar(dfg1, x="Stagione", y=['WH','N','WA'])
        dfg1_gr.update_layout(xaxis=dict(title="Stagione", type="category"),yaxis=dict(title="% W H/A"))
        st.plotly_chart(dfg1_gr)
    with st.expander('Gol 1/2 Tempo'):
        st.markdown("*Si è sempre segnato di più nel secondo tempo rispetto al primo?*")
        marcatori['Stagione']=[x[:4]+'-'+x[4:6] for x in marcatori['ID']]
        marcatori['Gol 1T']=[100 if x<=45 else 0 for x in marcatori['Minuto']]
        marcatori['Gol 2T'] = [100 if x > 45 else 0 for x in marcatori['Minuto']]
        df2=marcatori.groupby(['Stagione'],as_index=False).agg({'Gol 1T':'mean','Gol 2T':'mean'})
        df2_gr = px.bar(df2, x="Stagione", y=['Gol 1T','Gol 2T'])
        df2_gr.update_layout(xaxis=dict(title="Stagione", type="category"), yaxis=dict(title="% Gol 1T/2T"))
        st.plotly_chart(df2_gr)

with rec:
    st.markdown("*Record tutt'ora imbattuti in Serie A*")
    storico['diff_gol']=[x-y for x,y in zip(storico['GC'],storico['GT'])]
    storico['sum_gol'] = [x + y for x, y in zip(storico['GC'], storico['GT'])]
    dfs=storico.sort_values('diff_gol')
    dfg = storico.sort_values('sum_gol',ascending=False)
    wmore = dfg.iloc[0, :]
    wt=dfs.iloc[0,:]
    wc = dfs.iloc[dfs.shape[0]-1, :]
    daymore=storico.groupby(['Stagione','Giornata'],as_index=False).agg({'sum_gol':'sum'})
    daymore1 = daymore.sort_values('sum_gol', ascending=False)
    dm = daymore1.iloc[0, :]
    st.write(f"Vittoria più larga in casa: {wc['CASA']} - {wc['TRAS']} {wc['GC'].item()}-{wc['GT'].item()} - {wc['Giornata'].item()}° giornata - {wc['Giorno']}")
    st.write(f"Vittoria più larga in trasferta: {wt['CASA']} - {wt['TRAS']} {wt['GC'].item()}-{wt['GT'].item()} - {wt['Giornata'].item()}° giornata - {wt['Giorno']}")
    st.write(f"Partita con più gol: {wmore['CASA']} - {wmore['TRAS']} {wmore['GC'].item()}-{wmore['GT'].item()} - {wmore['Giornata'].item()}° giornata - {wmore['Giorno']}")
    st.write(f"Giornata con più gol: {dm['Giornata'].item()}° giornata della stagione {dm['Stagione']} con {dm['sum_gol'].item()} gol")

