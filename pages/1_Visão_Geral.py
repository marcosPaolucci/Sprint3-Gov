import streamlit as st
import plotly.express as px
from sklearn.metrics import precision_score, recall_score, confusion_matrix
from utils import dataframe_to_csv_button

st.set_page_config(page_title="Visão Geral", layout="wide")

st.title("Visão Geral do Piloto")
st.markdown("KPIs chave do piloto, metas vs. realizado e tendências temporais.")

# Verificar se o dataframe filtrado existe na sessão
if 'df_filtered' not in st.session_state or st.session_state.df_filtered.empty:
    st.warning("Não há dados para exibir. Por favor, ajuste os filtros na página inicial.")
    st.stop()

df = st.session_state.df_filtered

# Metas (mock)
metas = {
    'precisao': 0.85,
    'recall': 0.80,
    'fpr': 0.10
}

# Calcular KPIs
y_true = df['ground_truth']
y_pred = df['predicao']

precisao = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
fpr = fp / (fp + tn)
fnr = fn / (fn + tp)
total_tickets = len(df)
total_devolucoes_sem_acao = df['devolucoes_sem_acao'].sum()
total_devolucoes_com_acao = df['devolucoes_com_acao'].sum()
devolucoes_evitadas = total_devolucoes_sem_acao - total_devolucoes_com_acao

# Layout de KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Precisão", f"{precisao:.2%}", f"Meta: {metas['precisao']:.0%}")
col2.metric("Recall (Sensibilidade)", f"{recall:.2%}", f"Meta: {metas['recall']:.0%}")
col3.metric("Taxa de Falsos Positivos (FPR)", f"{fpr:.2%}", f"Meta: <{metas['fpr']:.0%}", delta_color="inverse")
col4.metric("Devoluções Evitadas", f"{devolucoes_evitadas}")

st.divider()

# Gráfico de Tendência Temporal
st.subheader("Tendência Temporal de Chamados e Fraudes")
df_temporal = df.set_index('timestamp').resample('D').agg({
    'id_chamado': 'count',
    'ground_truth': 'sum'
}).rename(columns={'id_chamado': 'Total de Chamados', 'ground_truth': 'Fraudes Reais'}).reset_index()

fig = px.line(df_temporal, x='timestamp', y=['Total de Chamados', 'Fraudes Reais'],
              title="Volume de Chamados vs. Fraudes Reais por Dia",
              labels={'value': 'Contagem', 'timestamp': 'Data'})
st.plotly_chart(fig, use_container_width=True)

# Anotações / Insights
st.subheader("Insights Rápidos")
regiao_mais_critica = df[df['ground_truth'] == 1]['regiao'].mode()[0]
st.info(f"💡 **Análise de Insights**: A região **{regiao_mais_critica}** concentra o maior número de ocorrências de fraude na seleção atual.")

# Download
dataframe_to_csv_button(df, "visao_geral.csv")