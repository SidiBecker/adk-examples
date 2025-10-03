from google.adk.agents import Agent
from multi_agent.gitlab_agent.agent import gitlab_sub_agent

# --- Definição do Agente Raiz ---

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    description="Agente principal que pode orquestrar outros subagentes.",
    instruction="Você é o agente principal. Use os subagentes disponíveis para responder às solicitações do usuário.",
    sub_agents=[gitlab_sub_agent]
)
