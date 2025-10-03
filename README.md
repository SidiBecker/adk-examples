# Agente de GitLab com Google ADK

Este projeto implementa um agente conversacional utilizando o framework `google-adk`. O agente é capaz de interagir com a API do GitLab para fornecer informações sobre branches e projetos configurados.

## Funcionalidades

O agente possui duas ferramentas principais:

1.  **`check_gitlab_branch`**: Verifica a existência de branches em projetos configurados. A busca aceita nomes parciais de branches (substrings).
2.  **`list_configured_projects`**: Lista todos os projetos que correspondem aos padrões de wildcard definidos na configuração.

## Configuração do Ambiente

Siga os passos abaixo para configurar e executar o projeto.

### 1. Criar e Ativar o Ambiente Virtual (.venv)

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```sh
# Crie o ambiente virtual na raiz do projeto
python -m venv .venv

# Ative o ambiente (Windows)
.venv\Scripts\activate
```

### 2. Instalar as Dependências

Com o ambiente ativado, instale as bibliotecas Python necessárias a partir do arquivo `requirements.txt`.

```sh
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente (.env)

O agente precisa de credenciais para acessar as APIs do Google e do GitLab. Crie um arquivo chamado `.env` dentro da pasta `gitlab_agent/`.

**Caminho do arquivo:** `gitlab_agent/.env`

Copie e cole o conteúdo abaixo no arquivo e substitua os valores de exemplo pelos seus.

```env
# URL da sua instância GitLab (ex: https://gitlab.com)
GITLAB_URL="https://gitlab.com"

# Seu Token de Acesso Pessoal do GitLab com escopo 'api'
GITLAB_PRIVATE_TOKEN="SEU_TOKEN_AQUI"

# Sua chave de API do Google AI Studio
GOOGLE_API_KEY="SUA_GOOGLE_API_KEY_AQUI"

# Lista de projetos ou padrões a serem pesquisados (um por linha, dentro das aspas)
# Wildcards (*) são suportados.
GITLAB_PROJECTS="grupo/subgrupo/projeto-*
outro-grupo/projeto-especifico
*nome-do-projeto*"
```

## Como Executar o Agente

Após configurar o ambiente, você pode iniciar o agente com o comando `adk run`. O `adk` encontrará e executará o `root_agent` definido em `gitlab_agent/agent.py`.

```sh
adk run gitlab_agent
```

O terminal deverá exibir uma mensagem de inicialização e aguardar seu comando.

## Exemplos de Uso

Uma vez que o agente esteja em execução, você pode fazer perguntas em linguagem natural:

**Para listar os projetos configurados:**

> "liste os projetos possíveis"

**Para verificar a existência de uma branch (busca exata):**

> "verifique a branch `main`"

**Para verificar a existência de uma branch (busca parcial):**

> "procure por branches com `feature/nova-tela`"

**Para sair do agente, pressione `Ctrl+C`.**
