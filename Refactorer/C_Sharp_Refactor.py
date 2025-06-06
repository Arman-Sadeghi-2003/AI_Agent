from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from dataclasses import dataclass
from typing import Optional
from pathlib import Path
from os.path import join
import os, httpx, asyncio, argparse

api_path = Path(__file__).resolve().parent.parent / 'Security' / 'APIs.txt'
api = api_path.read_text()

provider = GoogleProvider(api_key= api)
model = GoogleModel(model_name='gemini-2.0-flash', provider=provider)

system_prompt =  """
You are an AI agent tasked with processing and refactoring C# source code files. Your objectives are:

1. **Read C# Files**:
   - The user will provide a folder path.
   - Use the `readCSFile` function to read the contents of all `.cs` files in the specified folder.

2. **Refactor Code**:
   - Analyze the contents of each C# file individually.
   - Refactor the code to improve readability, maintainability, and performance while preserving original functionality.
   - Account for potential interdependencies between files to avoid breaking functionality.

3. **Add Documentation**:
   - For each method, add a comprehensive XML summary (`///`) that includes:
     - The method's purpose.
     - Parameters (if any) and their roles.
     - Return value (if applicable) and its meaning.
   - Add inline comments (`//`) to explain the logic of significant code blocks or lines.

4. **Write Refactored Files**:
   - Use the `Write_Refactored_cs_file` function to save the refactored code.
   - Create a new file for each original file, named with the same name plus `-refactored` (e.g., `OriginalFile.cs` becomes `OriginalFile-refactored.cs`).
   - Ensure output files are well-organized and maintain the original folder structure.

**Notes**:
- Process files individually but be aware of dependencies between files.
- Ensure refactored code is clean, follows C# best practices, and includes accurate documentation.
- If errors or ambiguities (e.g., missing dependencies or unclear code) are detected, include warnings or suggestions in the comments of the refactored file.
"""

@dataclass
class MyDeps:
    api: str
    http_client = httpx.AsyncClient

agent = Agent(model, system_prompt=system_prompt, deps_type=MyDeps)


@agent.tool
def readCSFile(ctx: RunContext[MyDeps], folder_name: str) -> dict[str,str]:
    contents = dict[str,str]()
    for root, _, files in os.walk(folder_name):
        for fileP in files:
            if not fileP.endswith('.cs'):
                continue
            file_path = join(root, fileP)
            try:
                content = Path(file_path).resolve().read_text(encoding='utf-8')
                contents[file_path] = content
            except Exception as e:
                print(f'File read error for {file_path}: {e}')
    return contents

@agent.tool
def Write_Refactored_cs_file(ctx: RunContext[MyDeps], contents: dict[str, str]):
    for file_path, new_content in contents.items():
        print(file_path)
        base, ext = os.path.splitext(file_path)
        if ext.lower() != '.cs':
            print(f"Skipping non-C# file: {file_path}")
            continue
        copy_path = f"{base}-refactored{ext}"
        try:
            with open(copy_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Refactored content written to: {copy_path}")
        except Exception as e:
            print(f"Failed to write to {copy_path}: {e}")

import argparse

async def main(folder_path: str):
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar')
        result = await agent.run(folder_path, deps=deps)
        print(result.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refactor C# files in a folder")
    parser.add_argument("folder", help="Path to the folder containing C# files")
    args = parser.parse_args()
    asyncio.run(main(args.folder))