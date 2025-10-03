
from google.adk.agents import Agent
import requests
import json

def get_dollar_quote():
    """
    Fetches the current USD to BRL exchange rate.
    """
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        brl_rate = data.get("rates", {}).get("BRL")
        if brl_rate:
            return {"status": "success", "report": f"A cotação do dólar hoje é R$ {brl_rate:.2f}."}
        else:
            return {"status": "error", "error_message": "Não foi possível obter a cotação do BRL."}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": str(e)}


dollar_sub_agent = Agent(
    name="dollar_sub_agent",
    model="gemini-2.5-flash",
    description="Subagente que obtém a cotação atual do dólar americano para o real brasileiro.",
    instruction="Sua tarefa é obter a cotação do dólar. Use a função get_dollar_quote para isso.",
    tools=[get_dollar_quote]
)

