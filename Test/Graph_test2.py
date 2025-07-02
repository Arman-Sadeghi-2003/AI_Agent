from pydantic import BaseModel, Field
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai import Agent, BinaryContent

from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the variables from the environment
model_name = 'gemini-2.5-flash'
api_path = Path(__file__).resolve().parent.parent / 'Security' / 'google.txt'
api_key = api_path.read_text()

# Create an instance of OpenAIModel using the loaded variables
vision_model = GoogleModel(
    model_name,
    provider=GoogleProvider(api_key=api_key),
)

analysis_model = GoogleModel(
    model_name,
    provider=GoogleProvider(api_key=api_key),
)

# Note for ollama both "minicpm-v" and "llama3.2-vision:latest" can't be used with pydantic tool calling, so we can't use it directly to call functions and format text
# therefor I will use 2 models, one for OCR and one for make structured data


class Item(BaseModel):
    item_name: str = Field(description="Item name")
    item_qu: str = Field(description="Quantity of item in the bill")
    item_price: str = Field(description="Price in $")

class BillSummary(BaseModel):
    items: list[Item] = Field(default_factory=list, description="List of items in the bill")
    subtotal: float = Field(description="Subtotal of the bill")
    tax: float = Field(description="taxes if applied bill")
    total: float = Field(description="total of the bill")
    bill_date: str = Field(description="bill issue date")
    bill_time: str = Field(description="bill issue time")

agent_vision = Agent(
    model=vision_model,
    result_retries = 3,
    system_prompt = "You are smart vision ai assistant, you will extract all text in any given image",
)

agent_analysis = Agent(
    model=analysis_model,
    result_type=BillSummary,
    result_retries = 3,
    system_prompt = "You are smart analysis agent, take the extracted OCR data, extract items and convert it to structured report",
)

# Process the receipt image
image_path = Path("./SampleData/grocery_test.png")
if image_path.exists():
    image_data = image_path.read_bytes()
    
    print("--------Running first Agent for OCR ---------")
    result_ocr_text = agent_vision.run_sync([
        "for the following receipt, do step by step extract all text and describe it in details",
        BinaryContent(data=image_data, media_type='image/png')
    ])
    print(result_ocr_text.output)

    print("\n--------Running second Agent for summarizing the extracted data ---------")
    result_structured = agent_analysis.run_sync(result_ocr_text.output)
    print(result_structured.output.model_dump_json(indent=2))
else:
    print("Error: grocery_test.png not found")