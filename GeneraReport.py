import base64
import os
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href
    

st.set_page_config(page_title="Genera Analisi sui tuoi dati in pochi click", page_icon="🔍", layout='wide', initial_sidebar_state='auto')
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.text("Carica qui sotto un file csv o xlsx")
#get file csv or excel in input with streamlit
file_upload = st.file_uploader("Carica il file csv o excel", type=["csv", "xlsx"])

df = None

#if file is not empty
if file_upload is not None:
    try:
        #if file is csv read it as csv
        if file_upload.lower().endswith("csv"):
            df = pd.read_csv(file_upload)
        #if file is excel read it as excel
        elif file_upload.lower().endswith("xlsx"):
            df = pd.read_excel(file_upload)
        #if file is not csv or excel show error
        else:
            st.error("File non valido")
    except :
        st.error("File non valido")
        
#create multiselect with all columns of dataframe
columns = st.multiselect("Seleziona le colonne da analizzare", df.columns)

try:
    #visualize dtaframe with aggrid in streamlit
    with st.expander("Visualizza dati in una tabella"):
        grid_response = AgGrid(
            df,
            columns=columns,
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
            editable=True,
            enable_enterprise_modules=True
        )
except:
    st.error("Errore nella visualizzazione dei dati")


try:
    #visulize descriptive statistics with aggrid in streamlit
    with st.expander("Visualizza statistiche descrittive"):
        grid_response = AgGrid(
            df.describe(),
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
            editable=True,
            enable_enterprise_modules=True
        )
except:
    st.error("Errore nella visualizzazione delle statistiche descrittive")

#create button
if st.button("Genera report") :
    with st.spinner("Generazione Report Corso..."):
        try:
            # create profile report with pandas_profiling and save it in html file
            profile = ProfileReport(df, title="Analisi dati by IntelligenzaArtificialeItalia.net", html_theme="dark")
            # save profile report in html file with name of file uploaded
            profile.to_file("Analisi_dati_IntelligenzaArtificialeItalia.net_" + file_upload.filename + ".html")
            # render profile report in streamlit
            st_profile_report(profile)

            st.markdown(get_binary_file_downloader_html("Analisi_dati_IntelligenzaArtificialeItalia.net_" + file_upload.filename + ".html", "Analisi_dati_IntelligenzaArtificialeItalia.net_" + file_upload.filename + ".html"))
            st.success("Report Generato Con Successo, per scaricarlo clicca il Link quì sopra.")

            st.balloons()
        except:
            st.error("Errore nella generazione del report")





