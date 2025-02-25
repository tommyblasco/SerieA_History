import streamlit as st

def load_data(n):
    l_data = st.connection(n, type=GSheetsConnection)
    l_data1 = l_data.read(worksheet="Foglio1")
    return l_data1

if "storico" not in st.session_state:
    st.session_state.storico = load_data(n="gspartite")

if "marcatori" not in st.session_state:
    st.session_state.marcatori = load_data(n="gsmarcatori")

storico=st.session_state.storico.copy()
marcatori=st.session_state.marcatori.copy()

storico['Data']=pd.to_datetime(storico['Data'], dayfirst=True)
storico['Giorno'] = storico['Data'].dt.strftime('%b %d, %Y')
storico['Data']=[x.date() for x in storico['Data']]
#storico['GC']=[int(x) for x in storico['GC']]
#storico['GT']=[int(x) for x in storico['GT']]
marcatori=marcatori[~marcatori['Minuto'].isna()]
marcatori['Minuto']=[int(x) for x in marcatori['Minuto']]
marcatori['Recupero']=[int(x) if not pd.isna(x) else np.nan for x in marcatori['Recupero'] ]
marcatori['Recupero'] = marcatori['Recupero'].astype('Int64')
