from openai import AsyncOpenAI
from config import AITOKEN

client = AsyncOpenAI(
    api_key=AITOKEN,
    base_url="https://openrouter.ai/api/v1"
)

async def ai_generate(text: str) -> str:
    resp = await client.chat.completions.create(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=[{"role": "user", "content": text}],
        temperature=0.8
    )
    return resp.choices[0].message.content
