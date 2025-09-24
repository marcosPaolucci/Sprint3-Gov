import streamlit as st
import plotly.graph_objects as go
from utils import dataframe_to_csv_button

st.set_page_config(page_title="Negócio e ROI", layout="wide")

st.title("Análise de Negócio e Retorno sobre o Investimento (ROI)")
st.markdown("Comparativo do impacto da solução de fraude e recomendação estratégica.")

if 'df_filtered' not in st.session_state or st.session_state.df_filtered.empty:
    st.warning("Não há dados para exibir.")
    st.stop()

df = st.session_state.df_filtered

# Cálculos para o comparativo
# Cenário SEM AÇÃO
total_chamados_sem_acao = len(df)
total_devolucoes_sem_acao = df['devolucoes_sem_acao'].sum()
valor_devolvido_sem_acao = (df['devolucoes_sem_acao'] * df['valor_produto']).sum()
custo_suporte_sem_acao = df['custo_total_sem_acao'].sum()
custo_total_sem_acao = valor_devolvido_sem_acao + custo_suporte_sem_acao

# Cenário COM AÇÃO
total_chamados_com_acao = len(df)
total_devolucoes_com_acao = df['devolucoes_com_acao'].sum()
valor_devolvido_com_acao = (df['devolucoes_com_acao'] * df['valor_produto']).sum()
custo_suporte_com_acao = df['custo_total_com_acao'].sum()
custo_total_com_acao = valor_devolvido_com_acao + custo_suporte_com_acao

# Resultados
economia_bruta = custo_total_sem_acao - custo_total_com_acao
investimento_piloto = 50000  # Mock
roi = (economia_bruta - investimento_piloto) / investimento_piloto if investimento_piloto > 0 else 0

st.header("Comparativo: Com Ação do Modelo vs. Sem Ação")

col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ Cenário SEM Ação")
    st.metric("Custo Total", f"R$ {custo_total_sem_acao:,.2f}")
    st.write(f"**Devoluções por Fraude**: {total_devolucoes_sem_acao}")
    st.write(f"**Valor Perdido em Devoluções**: R$ {valor_devolvido_sem_acao:,.2f}")
    st.write(f"**Custo de Suporte**: R$ {custo_suporte_sem_acao:,.2f}")


with col2:
    st.subheader("✅ Cenário COM Ação")
    st.metric("Custo Total", f"R$ {custo_total_com_acao:,.2f}", f"Economia de R$ {economia_bruta:,.2f}")
    st.write(f"**Devoluções por Fraude**: {total_devolucoes_com_acao}")
    st.write(f"**Valor Perdido em Devoluções**: R$ {valor_devolvido_com_acao:,.2f}")
    st.write(f"**Custo de Suporte**: R$ {custo_suporte_com_acao:,.2f}")

st.divider()

# ROI e Recomendação
st.header("Análise de ROI e Recomendação Executiva")

col_roi, col_rec = st.columns(2)

with col_roi:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=roi * 100,
        title={'text': "Retorno sobre Investimento (ROI)"},
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': '%'},
        gauge={'axis': {'range': [-50, 100]},
               'bar': {'color': "#0072C6"},
               'steps': [
                   {'range': [-50, 0], 'color': 'lightgray'},
                   {'range': [0, 50], 'color': 'gray'}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 20}}
    ))
    st.plotly_chart(fig, use_container_width=True)

with col_rec:
    st.subheader("Recomendação Go/No-Go")
    if roi > 0.20: # Limiar de 20%
        st.success("✔️ RECOMENDAÇÃO: GO")
        st.markdown("""
        O piloto demonstrou um ROI positivo, superando o limiar de 20%. A economia gerada pela redução de devoluções fraudulentas justifica o investimento na expansão da solução.
        
        **Próximos Passos Sugeridos:**
        1. Integrar o modelo aos sistemas de produção.
        2. Expandir o escopo para outras linhas de produto.
        3. Iniciar o desenvolvimento de um modelo v2 com machine learning.
        """)
    else:
        st.error("❌ RECOMENDAÇÃO: NO-GO (ou reavaliar)")
        st.markdown("""
        O ROI do piloto não atingiu o limiar mínimo de 20%. A economia gerada não compensa o investimento no momento.
        
        **Próximos Passos Sugeridos:**
        1. Revisar o modelo para melhorar a precisão e reduzir custos com falsos positivos.
        2. Reavaliar o custo-benefício em um cenário com maior volume de dados.
        3. Considerar um piloto estendido antes da decisão final.
        """)
        
dataframe_to_csv_button(df, "dados_roi.csv")