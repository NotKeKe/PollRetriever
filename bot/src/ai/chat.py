from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=...,
    base_url=...
)

async def str_to_time(string: str):
    ...