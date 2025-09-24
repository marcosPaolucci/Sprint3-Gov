import streamlit as st
import pandas as pd
from utils import load_data, local_css

st.set_page_config(
    page_title="Dashboard de Fraudes",
    page_icon="🛡️",
    layout="wide"
)

# Carregar CSS
local_css("style.css")

# Carregar dados
df = load_data()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros Dinâmicos")

# Converte a coluna de timestamp para datetime, se necessário
if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
    df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filtro de Período
min_date = df['timestamp'].min().date()
max_date = df['timestamp'].max().date()
date_range = st.sidebar.date_input(
    "Selecione o Período",
    (min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
start_date, end_date = date_range

# Filtro de Região/UF
regiao = st.sidebar.multiselect(
    "Selecione a Região",
    options=df['regiao'].unique(),
    default=df['regiao'].unique()
)

# Filtro de Linha de Produto
produto = st.sidebar.multiselect(
    "Selecione a Linha de Produto",
    options=df['linha_produto'].unique(),
    default=df['linha_produto'].unique()
)

# Filtro de Canal
canal = st.sidebar.multiselect(
    "Selecione o Canal",
    options=df['canal'].unique(),
    default=df['canal'].unique()
)

# Filtro de Original x Genérico
originalidade = st.sidebar.multiselect(
    "Original vs. Genérico",
    options=df['original_vs_generico'].unique(),
    default=df['original_vs_generico'].unique()
)

# Filtro de Severidade do Chamado
severidade = st.sidebar.multiselect(
    "Selecione a Severidade",
    options=df['severidade_chamado'].unique(),
    default=df['severidade_chamado'].unique()
)

# Aplicar filtros ao dataframe
df_filtered = df[
    (df['timestamp'].dt.date >= start_date) &
    (df['timestamp'].dt.date <= end_date) &
    (df['regiao'].isin(regiao)) &
    (df['linha_produto'].isin(produto)) &
    (df['canal'].isin(canal)) &
    (df['original_vs_generico'].isin(originalidade)) &
    (df['severidade_chamado'].isin(severidade))
]

# Armazenar dataframe filtrado no estado da sessão para uso em outras páginas
st.session_state.df_filtered = df_filtered

# --- CONTEÚDO DA PÁGINA PRINCIPAL ---
st.title("🛡️ Dashboard de Monitoramento de Fraudes")
st.markdown("### Bem-vindo ao centro de controle do piloto de detecção de fraudes.")
st.markdown("""
Use os filtros na barra lateral à esquerda para explorar os dados do piloto. Navegue pelas páginas para obter insights sobre a performance do modelo, governança e o impacto no negócio.
- **Visão Geral**: KPIs principais e tendências.
- **Detecção e Operação**: Análise aprofundada da performance do modelo.
- **Governança e Fairness**: Transparência sobre o funcionamento e viés do modelo.
- **Negócio e ROI**: Impacto financeiro e recomendação estratégica.
- **Mapa de Incidência**: Visualização geográfica das suspeitas de fraude.
""")

st.divider()

# Preparar o DataFrame para exibição
df_display = df_filtered.copy()

# Filtro específico por ID do Chamado
st.subheader("Explorar Registros")
id_busca = st.number_input(
    "Buscar por ID do Chamado (deixe em 0 para ver todos)",
    min_value=0,
    max_value=int(df_display['id_chamado'].max()),
    step=1,
    help="Digite o ID exato do chamado que deseja localizar."
)

# Mensagem informativa com a contagem total ANTES de filtrar por ID
st.info(f"**{len(df_display)}** registros selecionados com base nos filtros da barra lateral.")

# Aplicar o filtro por ID se um valor for inserido
if id_busca > 0:
    df_display = df_display[df_display['id_chamado'] == id_busca]
    if df_display.empty:
        st.warning(f"Nenhum registro encontrado com o ID {id_busca} nos dados filtrados.")
    else:
        st.success(f"Exibindo o registro para o ID {id_busca}.")

# Exibir o DataFrame com altura controlada e largura total
st.dataframe(df_display, height=800, use_container_width=True)