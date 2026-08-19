import os
from pathlib import Path


def load_env(path):
    """Load simple KEY=VALUE pairs without overriding real environment variables."""
    env_path = Path(path)
    if not env_path.is_file():
        return

    with env_path.open(encoding="utf-8-sig") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if value[:1] == value[-1:] and value.startswith(("'", '"')):
                value = value[1:-1]

            if key:
                os.environ.setdefault(key, value)
