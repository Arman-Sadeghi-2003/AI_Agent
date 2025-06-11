from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from dataclasses import dataclass
from pathlib import Path

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'google.txt'
api_key = api_path.read_text()

googleModel = GoogleModel('gemini-2.0-flash-exp', GoogleProvider(api_key=api_key))
class MyDeps:
    model: GoogleModel = googleModel
    
joke_selection_agent = Agent(model= googleModel,deps_type=MyDeps,
                             system_prompt= {
                                'Use the `joke_factory` to generate some jokes, then choose the best. '
                                'You must return just a single joke.'
                             })
