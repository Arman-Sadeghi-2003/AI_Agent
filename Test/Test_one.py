from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.models.google import GoogleModel
from pydantic_ai import Agent
from pathlib import Path

api_path = Path(__file__).resolve().parent.parent / "Security" / "APIs.txt"
api_key = api_path.read_text().strip()

provider = GoogleProvider(api_key=api_key)
google_model = GoogleModel("gemini-1.5-flash", provider = provider)
agent = Agent(
    google_model, 
    system_prompt="Be concise, reply with one sentence."
)

result = agent.run_sync('Where does "hello world" come from?')
print(result.output)

"""
The first known use of "hello, world" was in a 1974 textbook about the C programming language.
"""