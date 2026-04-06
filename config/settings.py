from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_token: str = ""
    github_api_url: str = "https://api.github.com"

    class Config:
        env_file = ".env"


settings = Settings()


if not settings.github_token:
    # Backward compatibility: support .env containing only a raw token string.
    env_path = Path(".env")
    if env_path.exists():
        first_line = env_path.read_text(encoding="utf-8").strip().splitlines()
        if first_line:
            token_candidate = first_line[0].strip()
            if token_candidate and "=" not in token_candidate:
                settings.github_token = token_candidate

if not settings.github_token:
    raise ValueError(
        "Missing GitHub token. Set GITHUB_TOKEN in .env or place the raw token as the first line."
    )