# Exemplos ADK - Sistema Multiagente

Este repositório contém exemplos de um sistema multiagente desenvolvido usando Python.

## Sobre o Projeto

Este projeto demonstra a implementação de um sistema multiagente em Python. Ele é estruturado para incluir diferentes tipos de agentes, cada um com responsabilidades específicas:

- **Agentes:** O diretório `multi_agent/` abriga a lógica central do sistema multiagente.
  - **Dollar Agent (`dollar_agent/`):** Provavelmente um agente responsável por tarefas relacionadas a moedas, como a obtenção de taxas de câmbio do dólar.
  - **GitLab Agent (`gitlab_agent/`):** Um agente projetado para interagir com a plataforma GitLab, podendo realizar ações como obter informações de projetos ou gerenciar issues.

## Requisitos de Instalação

Para configurar e executar este projeto, siga os passos abaixo:

1.  **Clonar o repositório:**
    ```bash
    git clone https://github.com/your-username/adk-examples.git
    cd adk-examples
    ```
2.  **Configurar o ambiente virtual:**
    É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto.
    ```bash
    python -m venv .venv
    # No Windows, ative com:
    .venv\Scripts\activate
    # No macOS/Linux, ative com:
    source .venv/bin/activate
    ```
3.  **Instalar as dependências:**
    Com o ambiente virtual ativado, instale todas as bibliotecas Python necessárias listadas no arquivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Como Executar

Execute o projeto com `adk run multi_agent`. Para sair pressione `Ctrl + C`.
