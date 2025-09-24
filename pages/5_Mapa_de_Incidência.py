import streamlit as st
import plotly.express as px
from utils import get_br_states_json, dataframe_to_csv_button

st.set_page_config(page_title="Mapa de Incidência", layout="wide")

st.title("Mapa de Incidência de Fraudes")
st.markdown("Distribuição geográfica das suspeitas de fraude para identificar hotspots.")

# Carregar o seu arquivo GeoJSON
geojson = get_br_states_json()

if geojson is None:
    st.error("Arquivo 'br_states.json' não encontrado. Certifique-se de que ele está na pasta correta.")
    st.stop()

if 'df_filtered' not in st.session_state or st.session_state.df_filtered.empty:
    st.warning("Não há dados para exibir. Por favor, ajuste os filtros na página inicial.")
    st.stop()

df = st.session_state.df_filtered

# Agregar dados por estado (UF)
fraudes_por_uf = df[df['ground_truth'] == 1].groupby('uf')['id_chamado'].count().reset_index()
fraudes_por_uf.rename(columns={'id_chamado': 'Contagem de Fraudes'}, inplace=True)

# Garantir que a coluna de localização seja do tipo string
fraudes_por_uf['uf'] = fraudes_por_uf['uf'].astype(str)

if fraudes_por_uf.empty:
    st.warning("Não há ocorrências de fraude nos dados filtrados para exibir no mapa.")
    st.stop()

# Criar o mapa coroplético
fig = px.choropleth(
    fraudes_por_uf,
    geojson=geojson,
    locations='uf',
    featureidkey="properties.SIGLA",
    color='Contagem de Fraudes',
    color_continuous_scale="Reds",
    scope="south america", # Define a visão geral do mapa
    labels={'Contagem de Fraudes': 'Fraudes'}
)

# A linha "fitbounds" foi REMOVIDA. Agora o layout geral será mantido.
fig.update_layout(
    title_text="Incidência de Fraudes por Estado",
    margin={"r":0, "t":40, "l":0, "b":0},
    geo=dict(
        showland=True, landcolor="rgb(217, 217, 217)",
        subunitwidth=1, subunitcolor="rgb(255, 255, 255)"
    )
)


st.plotly_chart(fig, use_container_width=True)

st.info("Passe o mouse sobre os estados para ver a contagem de fraudes. Estados mais escuros indicam maior incidência.")

dataframe_to_csv_button(fraudes_por_uf, "dados_mapa.csv")