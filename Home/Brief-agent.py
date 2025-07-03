from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pathlib import Path

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'openai_ai_news.txt'
api_key = api_path.read_text()

model = OpenAIModel(model_name='gpt-4o', provider=OpenAIProvider(api_key=api_key))

Brief_agent = Agent(model=model, 
                        system_prompt="You are a brief agent and you will give the EN sentence then get a"
                        "Brief of that and after that translate it to the Persian language. choose a file name for that content."
                        "use a line with (-) for separate the EN and IR contents."
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
How are memories stored and retrieved?

When you learn a new fact, like someone’s name, there are physical changes in the structure of your brain. But we don’t yet comprehend exactly what those changes are, how they are orchestrated across vast seas of synapses and neurons, how they embody knowledge, or how they are read out decades later for retrieval.

One complication is that there are many kinds of memories. The brain seems to distinguish short-term memory (remembering a phone number just long enough to dial it) from long-term memory (what you did on your last birthday). Within long-term memory, declarative memories (like names and facts) are distinct from non­declarative memories (riding a bicycle, being affected by a subliminal message), and within these general categories are numerous subtypes. Different brain structures seem to support different kinds of learning and memory; brain damage can lead to the loss of one type without disturbing the others.

Nonetheless, similar molecular mechanisms may be at work in these memory types. Almost all theories of memory propose that memory storage depends on synapses, the tiny connections between brain cells. When two cells are active at the same time, the connection between them strengthens; when they are not active at the same time, the connection weakens. Out of such synaptic changes emerges an association. Experience can, for example, fortify the connections between the smell of coffee, its taste, its color, and the feel of its warmth. Since the populations of neurons connected with each of these sensations are typically activated at the same time, the connections between them can cause all the sensory associations of coffee to be triggered by the smell alone.

But looking only at associations — and strengthened connections between neurons — may not be enough to explain memory. The great secret of memory is that it mostly encodes the relationships between things more than the details of the things themselves. When you memorize a melody, you encode the relationships between the notes, not the notes per se, which is why you can easily sing the song in a different key.

Memory retrieval is even more mysterious than storage. When I ask if you know Alex Ritchie, the answer is immediately obvious to you, and there is no good theory to explain how memory retrieval can happen so quickly. Moreover, the act of retrieval can destabilize the memory. When you recall a past event, the memory becomes temporarily susceptible to erasure. Some intriguing recent experiments show it is possible to chemically block memories from reforming during that window, suggesting new ethical questions that require careful consideration.
'''

result = Brief_agent.run_sync(content)
print(result.output)