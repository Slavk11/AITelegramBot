from openai import AsyncOpenAI
from config import AITOKEN

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AITOKEN,
)

async def ai_generate(text: str) -> str:
    completion = await client.chat.completions.create(
        model='deepseek/deepseek-chat',
        messages=[
            {
                "role": "user",
                "content": text
            }
        ]
    )

    print(completion)
    return completion.choices[0].message.content