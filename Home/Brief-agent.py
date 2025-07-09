from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pathlib import Path

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'openai_ai_news.txt'
api_key = api_path.read_text()
model = OpenAIModel(model_name='gpt-4o', provider=OpenAIProvider(api_key=api_key))

agp = Path(__file__).resolve().parent.parent / 'Security' / 'google.txt'
aga = agp.read_text()
gmodel = GoogleModel('gemini-2.0-flash', provider=GoogleProvider(api_key=aga))


Brief_agent = Agent(model=gmodel, 
                        system_prompt="You are a brief agent and you will give a part of EN article then get a"
                        "Brief and useful content of that and after that translate it to the Persian language. choose a file name for that content."
                        "use a line separator for storing both the EN and IR contents in a single file. But remember add orginal article on top of the Briefed"
                        "The final result of the content should be like this: orginal article - EN brief - Translate FA Brief"
                        "Use 'Writer' tool for write final content both En and IR in a file"
                        )

@Brief_agent.tool_plain
def Writer(briefedContent: str,fileName: str):
    try:
        path = Path('D:\Researches\Brain') / f'{fileName}.txt'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(briefedContent)
    except Exception:
        print(Exception)

content = '''
When a fire chief encounters a new blaze, he quickly makes predictions about how to best position his men. Running such simulations of the future — without the risk and expense of actually attempting them — allows “our hypotheses to die in our stead,” as philosopher Karl Popper put it. For this reason, the emulation of possible futures is one of the key businesses that intelligent brains invest in.

Yet we know little about how the brain’s future simulator works because traditional neuroscience technologies are best suited for correlating brain activity with explicit behaviors, not mental emulations. One idea suggests that the brain’s resources are devoted not only to processing stimuli and reacting to them (watching a ball come at you) but also to constructing an internal model of that outside world and extracting rules for how things tend to behave (knowing how balls move through the air). Internal models may play a role not only in motor acts, like catching, but also in perception. For example, vision draws on significant amounts of information in the brain, not just on input from the retina. Many neuroscientists have suggested over the past few decades that perception arises not simply by building up bits of data through a hierarchy but rather by matching incoming sensory data against internally generated expectations.

But how does a system learn to make good predictions about the world? It may be that memory exists only for this purpose. This is not a new idea: Two millennia ago, Aristotle and Galen emphasized memory as a tool in making successful predictions for the future. Even your memories about your life may come to be understood as a special subtype of emulation, one that is pinned down and thus likely to flow in a certain direction.
'''

result = Brief_agent.run_sync(content)
print(result.output)
