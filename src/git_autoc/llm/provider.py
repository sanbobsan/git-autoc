import logging

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from git_autoc.core.config import settings

logger = logging.getLogger(__name__)


def generate(messages: list[ChatCompletionMessageParam]) -> str:
    api_key = settings.openai_api_key or "sk-no-key-required"
    client = OpenAI(
        base_url=settings.openai_base_url,
        api_key=api_key,
    )

    for attempt in range(2):
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=settings.openai_temperature,
            max_tokens=settings.openai_max_tokens,
        )

        content = response.choices[0].message.content
        if content:
            return content

        logger.warning(
            "Empty response from model %s (attempt %d)",
            settings.openai_model,
            attempt + 1,
        )

    raise RuntimeError(
        f"Empty response from model {settings.openai_model} after 2 attempts"
    )
