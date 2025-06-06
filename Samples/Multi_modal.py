from pydantic_ai import Agent, DocumentUrl, ImageUrl
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel
from datetime import datetime as dt
from pathlib import Path

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'Pydantic.txt'
api = api_path.read_text()

model = OpenAIResponsesModel('', provider=OpenAIProvider(api_key=api))

class User(BaseModel):
    name: str
    age: int
    job: str
    
agent = Agent(model=model)

@agent.tool_plain
def get_current_time() -> dt:
    return dt.now()

@agent.tool_plain
def get_user() -> User:
    return User(name="Arman Sadeghi", age=22, job="Developer")

@agent.tool_plain
def get_funny_image() -> ImageUrl:
    return ImageUrl(url='https://iili.io/3Hs4FMg.png')

@agent.tool_plain
def get_document() -> DocumentUrl:
    return DocumentUrl(url='https://ai.pydantic.dev/tools/#function-tool-output')


result = agent.run_sync('What time is it?')
print(result.output)

result = agent.run_sync('What is the user name?')
print(result.output)

result = agent.run_sync('What is the image about?')
print(result.output)

result = agent.run_sync('What is the summary content of the document?')
print(result.output)