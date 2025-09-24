# Dashboard de Monitoramento de Fraudes - Sprint 3

Este projeto é uma aplicação web interativa construída com Streamlit para monitorar um piloto de detecção de fraudes. O dashboard consolida métricas de performance do modelo, governança, fairness e impacto de negócio (ROI).

## Estrutura do Projeto

- **`Home.py`**: Página inicial e script principal que executa os filtros laterais.
- **`data_generator.py`**: Módulo para gerar dados sintéticos para simulação.
- **`utils.py`**: Funções de utilidade, como carregamento de dados e formatação.
- **`get_json.py`**: Script para baixar o arquivo GeoJSON dos estados brasileiros.
- **`br_states.json`**: Arquivo de dados geográficos para o mapa de incidência.
- **`requirements.txt`**: Lista de dependências Python do projeto.
- **`style.css`**: Arquivo de estilos para customização da aparência.
- **`.streamlit/config.toml`**: Arquivo de configuração do Streamlit.
- **`pages/`**: Diretório contendo cada uma das páginas do dashboard.

## Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd nome_do_repositorio
    ```

2.  **Crie um ambiente virtual e instale as dependências:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run Home.py
    ```
    O dashboard estará acessível em seu navegador no endereço `http://localhost:8501`.

---

### Sobre o Arquivo de Mapa (`br_states.json`)

O arquivo `br_states.json`, necessário para a renderização do mapa de incidência, **já está incluído neste repositório**. Você não precisa baixá-lo manualmente para executar a aplicação.

Para fins de rastreabilidade e documentação, o script `get_json.py` também está disponível. Ele pode ser executado (`python get_json.py`) para baixar uma nova cópia do arquivo a partir de sua fonte original, caso seja necessário atualizá-lo no futuro.