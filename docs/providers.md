# Providers

git-autoc works with any OpenAI-compatible API. The only things it needs are a base URL, a model name, and optionally an API key, all set via the CLI or by editing `~/.config/git-autoc/config.toml`.

`openai_base_url` and `openai_model` are required and must be non-empty. `openai_api_key` is optional and can be left empty for local providers.

## Ollama

Run a local Ollama server and pull a model:

```bash
ollama pull llama3.2
ollama serve
```

Point git-autoc at it. Ollama uses the default `http://localhost:11434/v1`, so usually nothing needs changing:

```bash
git autoc config set openai_base_url
git autoc config set openai_model
```

Enter `http://localhost:11434/v1` for the base URL and `llama3.2` (or any pulled model) for the model. Leave the API key empty.

## LM Studio

Start the local server in LM Studio, then configure git-autoc:

```bash
git autoc config set openai_base_url
git autoc config set openai_model
```

Enter `http://localhost:1234/v1` for the base URL and the currently loaded model (shown in the LM Studio UI) for the model name. Leave the API key empty.

## OpenAI

```bash
git autoc config set openai_base_url
git autoc config set openai_model
git autoc config set openai_api_key
```

Enter `https://api.openai.com/v1`, a model such as `gpt-4o-mini`, and your OpenAI API key.

## Other providers

Any service exposing an OpenAI-compatible `/v1` endpoint works the same way: set `openai_base_url` to its base URL, `openai_model` to a model it serves, and `openai_api_key` if it requires one. This includes Mistral, Groq, Together, and self-hosted gateways.

## Example config

A full `config.toml` for a local Ollama setup looks like this:

```toml
openai_base_url = "http://localhost:11434/v1"  # Base URL of the OpenAI-compatible API
openai_model = "llama3.2"                      # Model name to use
openai_api_key = ""                            # API key (leave empty for local providers)
openai_temperature = 0.2                       # Sampling temperature (0-1, lower is more deterministic)
openai_max_tokens = 512                        # Maximum tokens to generate in the response
```
