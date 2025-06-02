from pydantic_ai import agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from pathlib import Path

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'APIs.txt'
api = api_path.read_text()
