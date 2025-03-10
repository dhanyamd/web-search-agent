from __future__ import annotations as _annotations
import asyncio
import os 
from dataclasses import dataclass 
from datetime import datetime 
from typing import Any 

import logfire 
from devtools import debug 
from httpx import AsyncClient 
from dotenv import load_dotenv 

from openai import AsyncOpenAI 
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent, ModelRetry, RunContext 

load_dotenv()
llm = os.getenv('LLM_MODEL', 'qwen2.5:32b')

client = AsyncOpenAI(
    base_url='http://localhost:11434/v1' ,# ur local ollama url
    api_key='ollama'
)
model = OpenAIModel(llm) if llm.lower().startswith("gpt") else OpenAIModel(llm, openai_client=client)
logfire.configure(send_to_logfire='if-token-present')

@dataclass
class Deps: 
    client: AsyncClient 
    brave_api_key: str | None 

web_search_agent = Agent(
    model,
    system_prompt=f'You are an expert at researching the web to answer user questions. The current date is: {datetime.now().strftime("%Y-%m-%d")}',
    deps_type=Deps,
    retries=2
)
async def main(): 
    pass  # Placeholder for the main function implementation

if __name__ == '__main__': 
    asyncio.run(main())  # Run the main function in the event loop