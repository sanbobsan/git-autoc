import logging

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    NotFoundError,
    OpenAI,
    RateLimitError,
)
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
        try:
            response = client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens,
            )
        except (APIConnectionError, APITimeoutError) as e:
            raise RuntimeError(
                f"Could not reach the API at {settings.openai_base_url}. "
                "Check that the server is running and the URL is correct, then "
                "run `git autoc config set openai_base_url`."
            ) from e
        except NotFoundError as e:
            raise RuntimeError(
                f"Model '{settings.openai_model}' not found at "
                f"{settings.openai_base_url}. "
                "Run `git autoc config set openai_model`."
            ) from e
        except AuthenticationError as e:
            raise RuntimeError(
                "The API rejected the API key. "
                "Run `git autoc config set openai_api_key`."
            ) from e
        except RateLimitError as e:
            raise RuntimeError(
                "The API is rate limiting requests. Try again in a moment."
            ) from e
        except APIStatusError as e:
            raise RuntimeError(
                f"API request failed with status {e.status_code} from "
                f"{settings.openai_base_url}."
            ) from e

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
