import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics import precision_score, recall_score
from utils import dataframe_to_csv_button

st.set_page_config(page_title="Governança e Fairness", layout="wide")

st.title("Análise de Fairness e Governança do Modelo")
st.markdown("Avaliação do desempenho do modelo em diferentes segmentos e documentação de transparência.")

if 'df_filtered' not in st.session_state or st.session_state.df_filtered.empty:
    st.warning("Não há dados para exibir.")
    st.stop()

df = st.session_state.df_filtered

# Análise de Fairness por corte
st.subheader("Desempenho por Segmento")
segmento = st.selectbox("Selecione o segmento para análise de fairness:", ('regiao', 'canal', 'linha_produto'))

metrics_by_segment = df.groupby(segmento).apply(
    lambda x: pd.Series({
        'precision': precision_score(x['ground_truth'], x['predicao'], zero_division=0),
        'recall': recall_score(x['ground_truth'], x['predicao'], zero_division=0),
        'count': len(x)
    })
).reset_index()

fig = px.bar(metrics_by_segment, x=segmento, y=['precision', 'recall'],
             barmode='group', title=f"Precisão e Recall por {segmento.capitalize()}",
             labels={'value': 'Score', segmento: segmento.capitalize()})
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Documentação de Governança
st.subheader("Documentação do Modelo (Model Card & LGPD)")

col1, col2 = st.columns(2)

with col1:
    with st.expander("📄 Model Card"):
        st.markdown("""
        - **Objetivo do Modelo**: Identificar proativamente chamados de suporte relacionados a produtos falsificados para reduzir devoluções e custos operacionais.
        - **Dados Utilizados**: Dados de chamados, incluindo região, canal de venda, tipo de produto e severidade. Nenhum dado pessoal sensível é utilizado.
        - **Limites de Uso**: O modelo serve como uma ferramenta de auxílio à decisão. Casos marcados como fraude devem ser revisados por um analista antes de qualquer ação com o cliente. O modelo não é treinado para detectar todos os tipos de fraude.
        - **Métricas de Performance**: O modelo é avaliado por Precisão, Recall e Taxa de Falsos Positivos (FPR).
        """)

with col2:
    with st.expander("⚖️ LGPD (Lei Geral de Proteção de Dados)"):
        st.markdown("""
        - **Base Legal**: O tratamento dos dados para detecção de fraude se enquadra na base legal de **legítimo interesse** (Art. 7º, IX) e **proteção ao crédito** (Art. 7º, X).
        - **Minimização de Dados**: Apenas dados não-pessoais e estritamente necessários para a análise de fraude são utilizados.
        - **Retenção de Dados**: Os dados agregados e os resultados do modelo são retidos por 24 meses para fins de auditoria e melhoria contínua. Dados brutos são anonimizados após 90 dias.
        - **Direitos do Titular**: O cliente pode solicitar a revisão de qualquer decisão automatizada através dos canais de suporte padrão.
        """)

dataframe_to_csv_button(metrics_by_segment, "dados_fairness.csv")