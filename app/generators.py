from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
)

async def ai_generate(text: str) -> str:
    # Вызов асинхронного метода создания completion
    completion = await client.chat.completions.create(
        model='deepseek/deepseek-chat',
        messages=[
            {
                "role": "user",
                "content": text
            }
        ]
    )

    # Посмотрим, что вернулось
    print(completion)

    # Вернём текстовый ответ
    return completion.choices[0].message.content