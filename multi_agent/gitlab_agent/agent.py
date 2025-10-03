from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
import gitlab
import os
from dotenv import load_dotenv
import fnmatch

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- LÓGICA COMPARTILHADA ---

def get_matched_projects(gl) -> set:
    """Busca e filtra projetos do GitLab de acordo com a lista de padrões no .env."""
    projects_str = os.getenv("GITLAB_PROJECTS", "")
    if not projects_str:
        raise ValueError("A variável GITLAB_PROJECTS não está definida no arquivo .env")

    # Converte a string multi-linha do .env em uma lista, ignorando linhas vazias
    PROJECTS = [line.strip() for line in projects_str.splitlines() if line.strip()]

    matched_projects = set()
    for pattern in PROJECTS:
        try:
            if "*" not in pattern:
                project = gl.projects.get(pattern)
                matched_projects.add(project)
            else:
                prefix = pattern.split('*', 1)[0]
                search_term = next((part for part in reversed(prefix.split('/')) if part), '')
                candidate_projects = gl.projects.list(search=search_term, all=True)
                for project in candidate_projects:
                    if fnmatch.fnmatch(project.path_with_namespace, pattern) or fnmatch.fnmatch(project.name, pattern):
                        matched_projects.add(project)
        except gitlab.exceptions.GitlabGetError as e:
            if e.response_code == 404:
                print(f"Aviso: O projeto ou padrão '{pattern}' não retornou resultados.")
                continue
            else:
                raise
    return matched_projects

# --- FERRAMENTAS DO AGENTE ---

def check_gitlab_branch(branch_substring: str) -> dict:
    """Verifica, usando parte do nome (substring), quais branches existem e em quais projetos."""
    try:
        gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), private_token=os.getenv("GITLAB_PRIVATE_TOKEN"))
        gl.auth()
        matched_projects = get_matched_projects(gl)
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

    if not matched_projects:
        return {"status": "success", "report": "Nenhum projeto correspondeu aos padrões definidos."}

    found_branches = []
    for project in matched_projects:
        try:
            project_branches = project.branches.list(all=True)
            for branch in project_branches:
                if branch_substring in branch.name:
                    found_branches.append({
                        "project": project.path_with_namespace,
                        "branch": branch.name
                    })
        except gitlab.exceptions.GitlabGetError:
            continue
    
    if found_branches:
        report_lines = [f"- Projeto: {found['project']}, Branch: {found['branch']}" for found in found_branches]
        report = f"Branches contendo '{branch_substring}' foram encontradas:\n" + "\n".join(report_lines)
    else:
        report = f"Nenhuma branch contendo '{branch_substring}' foi encontrada nos projetos correspondentes."
        
    return {"status": "success", "report": report}

def list_configured_projects() -> dict:
    """Lista todos os projetos GitLab que correspondem à configuração de padrões no .env."""
    try:
        gl = gitlab.Gitlab(os.getenv("GITLAB_URL"), private_token=os.getenv("GITLAB_PRIVATE_TOKEN"))
        gl.auth()
        matched_projects = get_matched_projects(gl)
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

    if not matched_projects:
        return {"status": "success", "report": "Nenhum projeto correspondeu aos padrões definidos na configuração."}

    project_paths = sorted([p.path_with_namespace for p in matched_projects])
    report = "Os seguintes projetos correspondem à sua configuração: \n- " + "\n- ".join(project_paths)
    return {"status": "success", "report": report}

# --- Definição do Agente ---

gitlab_sub_agent = Agent(
        name="gitlab_sub_agent",
        model="gemini-2.5-flash",
        description=(
            "Agente para interagir com o GitLab. Pode verificar a existência de branches ou listar os projetos configurados."
        ),
        instruction=(
            "Você é um agente prestativo que responde a perguntas sobre projetos do GitLab."
        ),
        tools=[check_gitlab_branch, list_configured_projects]
    )
