import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.metrics import confusion_matrix
import numpy as np
from utils import dataframe_to_csv_button

st.set_page_config(page_title="Detecção e Operação", layout="wide")

st.title("Análise de Detecção e Operação")
st.markdown("Métricas detalhadas sobre a performance do modelo e a eficiência operacional.")

if 'df_filtered' not in st.session_state or st.session_state.df_filtered.empty:
    st.warning("Não há dados para exibir. Por favor, ajuste os filtros na página inicial.")
    st.stop()

df = st.session_state.df_filtered

y_true = df['ground_truth']
y_pred = df['predicao']

# Matriz de Confusão
cm = confusion_matrix(y_true, y_pred)
tn, fp, fn, tp = cm.ravel()

# Renomear eixos
x = ['Não Fraude (Predito)', 'Fraude (Predito)']
y = ['Não Fraude (Real)', 'Fraude (Real)']
z = [[tn, fp], [fn, tp]]
z_text = [[str(y) for y in x] for x in z]

fig_cm = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Blues')
fig_cm.update_layout(title_text='<b>Matriz de Confusão</b>')


# KPIs Operacionais
tempo_medio_deteccao = df['tempo_deteccao_min'].mean()
fila_revisao_humana = df['revisado_por_humano'].sum()
taxa_override = df['override_humano'].sum() / fila_revisao_humana if fila_revisao_humana > 0 else 0

col1, col2 = st.columns([1, 1])

with col1:
    st.plotly_chart(fig_cm, use_container_width=True)

with col2:
    st.subheader("KPIs Operacionais")
    st.metric("Tempo Médio de Detecção", f"{tempo_medio_deteccao:.1f} minutos")
    st.metric("Casos para Revisão Humana", f"{fila_revisao_humana}")
    st.metric("Taxa de Override Humano", f"{taxa_override:.2%}")
    st.markdown("""
    - **Revisão Humana**: Quantidade de casos que passaram pelo crivo de um analista.
    - **Taxa de Override**: Percentual de casos em que o analista reverteu a decisão do modelo.
    """)

dataframe_to_csv_button(df, "dados_operacionais.csv")