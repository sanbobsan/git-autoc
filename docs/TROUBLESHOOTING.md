# Troubleshooting

Quick fixes for the messages git-autoc can print. Every fix uses `git autoc config` — run `git autoc config` first to see the current values.

## Error messages

| Message | Likely cause | Fix |
|---|---|---|
| `Could not reach the API at <url>` | Server is not running, or `openai_base_url` is wrong | Start the server; verify the URL with `curl` (see below); then `git autoc config set openai_base_url` |
| `Model '<model>' not found at <url>` | The model does not exist on the server, or the name is misspelled | Check available models (e.g. `ollama list`, `curl <url>/models`); `git autoc config set openai_model` |
| `The API rejected the API key` | Wrong or missing API key for a remote provider | `git autoc config set openai_api_key`; for local providers leave it empty |
| `The API is rate limiting requests` | Too many requests in a short time | Wait a moment and retry |
| `API request failed with status <n> from <url>` | The server returned an error | Check server logs; the status code is a clue (e.g. 400, 500, 503) |
| `Empty response from model <model> after 2 attempts` | The model returned no text twice | Pick a different model or check server logs |
| `Failed to read config file <path>: <e>` | `config.toml` is not valid TOML | Fix or recreate it: `git autoc config clear`, then `git autoc config` |
| `Missing required config: openai_base_url, openai_model` | One of the required keys is empty | `git autoc config set openai_base_url` and `git autoc config set openai_model` |
| `Unknown config key '<key>'` | Misspelled setting name | Use one of the documented keys in the README |
| `'<key>' expects an integer, got ...` | `openai_max_tokens` is not a whole number | `git autoc config set openai_max_tokens` with a value like `512` |
| `'<key>' expects a number, got ...` | `openai_temperature` is not a number | `git autoc config set openai_temperature` with a value like `0.2` |
| `No staged changes found` | There is nothing staged to generate a commit for | Stage files with `git add`, or answer `y` when git-autoc offers to stage everything |
| `Use only one of --long, --list, --desc` | More than one body-style flag given | Pass at most one of these flags |

## Verify the connection

Check that the API is reachable before blaming the configuration:

```bash
curl http://localhost:11434/v1/models
```

For a remote provider, pass the same URL you configured and add the API key header if needed. A `200` response with a JSON list of models means the endpoint is fine; then make sure `openai_model` matches one of those names.

