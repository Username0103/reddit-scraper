from __future__ import annotations

import pickle
import sys
from dataclasses import dataclass, fields

from reddit_scraper import DATA_DIR, CREDS_CACHE, DEFAULT_UA


@dataclass
class RedditCredentials:
    client_id: str | None
    api_key: str | None
    user_agent: str | None


def handle_credentials(args: RedditCredentials) -> RedditCredentials:
    cache: RedditCredentials
    EMPTY_CREDS = RedditCredentials(None, None, DEFAULT_UA)

    if not CREDS_CACHE.exists():
        cache = EMPTY_CREDS
    else:
        cache = pickle.loads(CREDS_CACHE.read_bytes())

    credentials = inspect_fields(args, cache)
    data = RedditCredentials(**credentials)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CREDS_CACHE.write_bytes(pickle.dumps(data))
    if args == EMPTY_CREDS:
        return data
    print("Succesfully set new credentials.")
    sys.exit(0)


def inspect_fields(args: RedditCredentials, cache: RedditCredentials) -> dict:
    credentials = {}
    for field in fields(RedditCredentials):
        name = field.name
        value_argv = getattr(args, name)
        value_cache = getattr(cache, name)
        if not value_argv and not value_cache:
            print(f"{name} not provided in args and not found in cache.")
            sys.exit(1)
        credentials[name] = value_argv or value_cache
    return credentials
