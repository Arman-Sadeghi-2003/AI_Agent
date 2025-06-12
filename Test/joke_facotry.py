from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from dataclasses import dataclass
from pathlib import Path

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'google.txt'
api_key = api_path.read_text()

googleModel = GoogleModel('gemini-2.0-flash-exp', provider=GoogleProvider(api_key=api_key))
    
joke_selection_agent = Agent(
    model=googleModel,
    system_prompt= {
        'Use the `joke_factory` to generate some jokes, then choose the best. '
        'You must return just a single joke.'
    }
)
joke_generator_agent = Agent(model=googleModel, output_type=list[str])

@joke_selection_agent.tool
async def joke_factory(ctx: RunContext[None], count: int) -> list[str]:
    r = await joke_generator_agent.run(
        f'Please generate {count} jokes. and use parrote, cat, and forest in that.',
        usage=ctx.usage
    ) 
    return r.output
    
result = joke_selection_agent.run_sync(
    'Tell me a joke.',
    usage_limits=UsageLimits(request_limit=5, total_tokens_limit=300)
)

print(result.output)
print(result.usage())