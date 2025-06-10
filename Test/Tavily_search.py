from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool
from pathlib import Path

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'apis.txt'
api = api_path.read_text()
T_api_path = Path(__file__).resolve().parent.parent / 'Security' / 'Tavily ai.txt'
t_api = T_api_path.read_text()

model = GoogleModel('gemini-2.0-flash', provider=GoogleProvider(api_key=api))

agent = Agent(model=model, 
              tools=[tavily_search_tool(api_key=t_api)],
              system_prompt='Search Tavily for the given query and return the results.')

result = agent.run_sync('Tell me the top news in the GenAI world, give me links.')

print(result.output)