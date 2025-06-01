from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_graph import BaseNode, GraphRunContext

from googlesearch import search
from newspaper import Article
from urllib.parse import urlparse
from dataclasses import dataclass
import httpx, os

from pathlib import Path

dir_name = str(Path(__file__).resolve().parent.parent / "final sites")
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

api_path = Path(__file__).resolve().parent.parent / "Security" / "APIs.txt"
api_key = api_path.read_text().strip()

provider = GoogleProvider(api_key=api_key)
google_model = GoogleModel('gemini-2.0-flash', provider = provider)
agent = Agent(
    google_model, 
     system_prompt="use 'get_top_10_sites' to find best and trenned sites about subject and " \
     "then use 'write_site_Details' function for write all summary about thoes sites one by one in to the seperated file. " \
    "Remember add site link at the end of the file." \
    "after all get a good summary of all results and then use 'Write_summary_of_document' function for write min:30 and max:45 lines of Brief and useful sentences about subject."
)

@agent.tool
def get_top_10_sites(ctx: RunContext[str], subject: str) -> list[str]:
    """
    Searches Google for a given subject and returns the top 10 URLs as a list of strings.
    
    :param subject: The search term or subject to look up.
    :return: List of 10 URLs (strings).
    """
    try:
        results = search(subject, num_results=10)
        return list(results)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

@agent.tool
def write_site_Details(ctx: RunContext[str], sites_summary: list[str]):
    i = 1
    for content in sites_summary:
        file_path = os.path.join(dir_name, f'site-{i}.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            i += 1

@agent.tool
def Write_summary_of_document(ctx: RunContext[str], brief_and_useful_text: str):
    file_path = os.path.join(dir_name, 'result.txt')
    with open(file_path, 'w') as f:
        f.write(brief_and_useful_text)

resutl = agent.run_sync('trenned companies at ai_agents')

print(resutl.output)