from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pathlib import Path
import random

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'APIs.txt'
api = api_path.read_text()

model = GoogleModel('gemini-2.0-flash-exp', provider=GoogleProvider(api_key=api))

agent = Agent(model, 
              deps_type=str,
              system_prompt=(
                  "You're a dice game, you should roll the die and see if the number you get "
                  "you get back matches the user's guess. If so, tell them they're a winner."
                  "Use the player's name in the response."
              ))

@agent.tool_plain
def roll_die() -> str:
    return str(random.randint(1, 6))

@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    return ctx.deps

user_name = input("What's your name?")
user_guess = int(input('Guess the die number:'))

result = agent.run_sync(f'I guess {user_guess}', deps=user_name)
print(result.output)