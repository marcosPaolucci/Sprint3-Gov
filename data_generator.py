import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Funções para gerar o DataFrame sintético
def generate_synthetic_data(start_date_str="2025-01-01", end_date_str="2025-09-23", num_rows=2500):
    """Gera um DataFrame de dados sintéticos para o dashboard."""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    data = {
        'id_chamado': range(1, num_rows + 1),
        'timestamp': [start_date + timedelta(seconds=np.random.randint(0, int((end_date - start_date).total_seconds()))) for _ in range(num_rows)],
        'regiao': np.random.choice(['Sudeste', 'Nordeste', 'Sul', 'Centro-Oeste', 'Norte'], num_rows, p=[0.4, 0.25, 0.15, 0.1, 0.1]),
        'uf': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'PE', 'RS', 'PR', 'GO', 'AM'], num_rows),
        'linha_produto': np.random.choice(['Cartucho', 'Toner'], num_rows, p=[0.7, 0.3]),
        'canal': np.random.choice(['E-commerce', 'Loja Física', 'Suporte Técnico'], num_rows, p=[0.6, 0.3, 0.1]),
        'original_vs_generico': np.random.choice(['Original', 'Genérico'], num_rows, p=[0.8, 0.2]),
        'severidade_chamado': np.random.choice(['Baixa', 'Média', 'Alta'], num_rows, p=[0.5, 0.3, 0.2]),
        'valor_produto': np.round(np.random.uniform(50, 800, num_rows), 2),
        'nps_score': np.random.randint(1, 11, num_rows),
        'tempo_deteccao_min': np.round(np.random.uniform(1, 60, num_rows)),
        'revisado_por_humano': np.random.choice([True, False], num_rows, p=[0.3, 0.7]),
    }
    df = pd.DataFrame(data)

    # Gerar ground_truth (se é fraude ou não) com viés regional
    conditions = [
        (df['regiao'] == 'Nordeste') & (df['original_vs_generico'] == 'Genérico'),
        (df['canal'] == 'E-commerce') & (df['valor_produto'] > 500)
    ]
    probabilities = [0.15, 0.10]
    base_fraud_prob = 0.05
    df['ground_truth'] = np.random.choice([1, 0], num_rows, p=[base_fraud_prob, 1-base_fraud_prob])
    for cond, prob in zip(conditions, probabilities):
        df.loc[cond, 'ground_truth'] = np.random.choice([1, 0], cond.sum(), p=[prob, 1-prob])

    # Simular predição do modelo com um viés realista (com alguns erros)
    df['probabilidade_fraude'] = df['ground_truth'] * np.random.uniform(0.7, 0.95, num_rows) + (1 - df['ground_truth']) * np.random.uniform(0.01, 0.2, num_rows)
    
    # Criar a predição base
    df['predicao'] = (df['probabilidade_fraude'] > 0.6).astype(int)

    # Introduzir erros para simular um modelo imperfeito
    # Introduzir Falsos Negativos (o modelo erra, não detecta a fraude)
    df.loc[df['ground_truth'] == 1, 'predicao'] = np.random.choice([1, 0], df[df['ground_truth'] == 1].shape[0], p=[0.90, 0.10])
    
    # Introduzir Falsos Positivos (o modelo erra, detecta fraude onde não tem)
    df.loc[df['ground_truth'] == 0, 'predicao'] = np.random.choice([0, 1], df[df['ground_truth'] == 0].shape[0], p=[0.99, 0.01])

    # Simular override humano
    df['override_humano'] = np.where(df['revisado_por_humano'] & (df['predicao'] != df['ground_truth']), True, False)

    # Simular cenários 'Com Ação' vs 'Sem Ação'
    df['custo_suporte'] = np.random.uniform(20, 50, num_rows)
    
    # Cenário 'Com Ação'
    df['custo_total_com_acao'] = df['custo_suporte']
    df.loc[(df['predicao'] == 1) & (df['ground_truth'] == 0), 'custo_total_com_acao'] += 30 # Custo de investigação de falso positivo
    df['devolucoes_com_acao'] = ((df['predicao'] == 0) & (df['ground_truth'] == 1)).astype(int) # Falso negativo -> devolução ocorreu

    # Cenário 'Sem Ação'
    df['custo_total_sem_acao'] = df['custo_suporte']
    df['devolucoes_sem_acao'] = df['ground_truth'] # Todas as fraudes viram devolução
    
    df['economia'] = (df['devolucoes_sem_acao'] * df['valor_produto'] + df['custo_total_sem_acao']) - \
                     (df['devolucoes_com_acao'] * df['valor_produto'] + df['custo_total_com_acao'])

    df['periodo'] = df['timestamp'].dt.to_period('M').astype(str)

    return df