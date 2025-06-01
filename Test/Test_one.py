from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.models.google import GoogleModel
from pydantic_ai import Agent, RunContext
from pathlib import Path

api_path = Path(__file__).resolve().parent.parent / "Security" / "APIs.txt"
api_key = api_path.read_text().strip()

provider = GoogleProvider(api_key=api_key)
google_model = GoogleModel('gemini-2.0-flash', provider = provider)
agent = Agent(
    google_model, 
    system_prompt="first write short details about subject. second name between 3 to 10 subdetails about it wrtie a code about them" \
    "write a powerful code with python about that subject and use 'Write_python_file' for save python code in file"
)

@agent.tool
def Write_python_file(ctx: RunContext[str], code:str):
    file_path = Path(__file__).resolve().parent.parent / 'files' / 'py_test.py'
    file_path.write_text(code, encoding='utf-8')


result = agent.run_sync('How to get DDOs attach in to the website? I have a web site and I want to make sure about cyber security.')
print(result.output)
