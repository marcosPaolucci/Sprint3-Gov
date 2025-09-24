# Dashboard de Monitoramento de Fraudes - Sprint 3

Este projeto é uma aplicação web interativa construída com Streamlit para monitorar um piloto de detecção de fraudes. O dashboard consolida métricas de performance do modelo, governança, fairness e impacto de negócio (ROI).

## Estrutura do Projeto

- **`Home.py`**: Página inicial e script principal que executa os filtros laterais.
- **`data_generator.py`**: Módulo para gerar dados sintéticos para simulação.
- **`utils.py`**: Funções de utilidade, como carregamento de dados e formatação.
- **`requirements.txt`**: Lista de dependências Python do projeto.
- **`style.css`**: Arquivo de estilos para customização da aparência.
- **`.streamlit/config.toml`**: Arquivo de configuração do Streamlit.
- **`pages/`**: Diretório contendo cada uma das páginas do dashboard.

## Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd novo_dashboard_fraude
    ```

2.  **Crie um ambiente virtual e instale as dependências:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Baixe o arquivo de mapa (necessário para a página 5):**
    - Acesse [este link](https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-35-mun.json) e salve o arquivo como `br_states.json` dentro do diretório principal do projeto.

4.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run Home.py
    ```

O dashboard estará acessível em seu navegador no endereço `http://localhost:8501`.
