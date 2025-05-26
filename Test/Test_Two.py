from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai import Agent, RunContext
from pathlib import Path

api_key_path = Path(__file__).resolve().parent.parent /'Security' / 'APIs.txt'
google_api_key = api_key_path.read_text().strip()

provider = GoogleProvider(api_key=google_api_key)
model = GoogleModel(model_name='gemini-1.5-flash', provider=provider)

roulette_agent = Agent(
    model=model,
    deps_type=int,
    output_type=bool,
    system_prompt=(
        'Use the `roulette_wheel` function to see if the customer has won' \
        ' based on the number they provide.'
    ),
)

@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
    """Check if the square is a winner."""
    return 'Winner ☻' if square == ctx.deps else 'Loser'

success_number = 18  
result = roulette_agent.run_sync('Put my money on square eighteen', deps=success_number)
print(result.output)  

result = roulette_agent.run_sync('I bet five is the winner', deps=success_number)
print(result.output)