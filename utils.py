import streamlit as st
import pandas as pd
from data_generator import generate_synthetic_data

@st.cache_data
def load_data():
    """Carrega e armazena em cache os dados sintéticos."""
    df = generate_synthetic_data()
    return df

def local_css(file_name):
    """Carrega um arquivo CSS local."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def get_br_states_json():
    """Carrega e armazena em cache o geojson dos estados brasileiros."""
    import json
    try:
        with open('br_states.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def dataframe_to_csv_button(df, filename="dados_filtrados.csv", label="Exportar para CSV"):
    """Gera um botão de download para um DataFrame em formato CSV."""
    @st.cache_data
    def convert_df(df_to_convert):
       return df_to_convert.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)
    st.download_button(
       label=label,
       data=csv,
       file_name=filename,
       mime='text/csv',
    )