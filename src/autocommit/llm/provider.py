from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from autocommit.core.config import settings


def generate(messages: list[ChatCompletionMessageParam]) -> str:
    api_key = settings.openai_api_key or "sk-no-key-required"
    client = OpenAI(
        base_url=settings.openai_base_url,
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=settings.openai_temperature,
        max_tokens=settings.openai_max_tokens,
    )

    content = response.choices[0].message.content
    return content or ""
