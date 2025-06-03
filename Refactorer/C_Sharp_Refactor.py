from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from pathlib import Path
from os.path import isfile, join
import os
import shutil

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'APIs.txt'
api = api_path.read_text()

provider = GoogleProvider(api_key= api)
model = GoogleModel(model_name='gemini-2.0-flash', provider=provider)
agent = Agent(model, system_prompt=(
    "user will gives you folder path and you should Read all cs file in it with 'readCSFile' function help and gives all thoes contents." \
    "You should refactore the contents, add comments on code, and add a full and clean XML summary on each method. " \
    "Then use 'Write_Refactored_cs_file' this function to write result in new file with same file name additional -refactored" \
    "may file had relate to eachother!"
))

@agent.tool
def readCSFile(ctx: RunContext[str], folder_name: str) -> dict[str,str]:
    onlyfiles = [f for f in os.listdir(folder_name) if isfile(join(folder_name, f))]
    contents = dict[str,str]()
    for fileP in onlyfiles:
        try:
            if not fileP.endswith('.cs'):
                continue
            fileP = join(folder_name, fileP)
            content = Path(fileP).resolve().read_text()
            contents[fileP] = content
        except Exception as e:
            print(f'File read error: {e}')
    return contents

@agent.tool
def Write_Refactored_cs_file(ctx: RunContext[str], contents: dict[str,str]):
     for file_path, new_content in contents.items():
        # Split path to get filename and extension
        base, ext = os.path.splitext(file_path)

        # Make sure we're working with a .cs file
        if ext.lower() != '.cs':
            print(f"[!] Skipping non-C# file: {file_path}")
            continue

        # Create copy path with '-copy' before the .cs extension
        copy_path = f"{base}-refactored{ext}"

        # Copy original file
        try:
            shutil.copy2(file_path, copy_path)
            print(f"[+] Created copy: {copy_path}")
        except Exception as e:
            print(f"[!] Failed to copy {file_path}: {e}")
            continue

        # Write new content to the copied file
        try:
            with open(copy_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[✓] Updated content written to: {copy_path}")
        except Exception as e:
            print(f"[!] Failed to write to {copy_path}: {e}")

res = agent.run_sync('G:\New folder')
print(res.output)