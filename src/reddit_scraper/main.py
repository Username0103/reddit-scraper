from __future__ import annotations

from dataclasses import dataclass
import sys

from reddit_scraper import logger, SORT_TYPE

from .get_credentials import RedditCredentials, handle_credentials, CREDS_CACHE
from .get_posts import get_posts, create_instance
from .database import append_db, DB, RedditComment, RedditPost


@dataclass
class Options:
    loglevel: int | None
    subreddit: str
    num_posts: int
    to_clear: bool
    skip_comments: bool
    sort_type: SORT_TYPE
    creds: RedditCredentials


def check_options(args: Options) -> None:
    if args.to_clear:
        if CREDS_CACHE.exists():
            CREDS_CACHE.unlink()
            print("Succesfully cleared credentials cache")
            sys.exit(0)
        print("Did not succesfully cleared credentials cache, as they did not exist.")
        sys.exit(1)


def run(args: Options) -> None:
    logger.info("Program has started up.")
    check_options(args)
    if CREDS_CACHE.exists():
        logger.debug(f"Program is using cached credentials from {str(CREDS_CACHE)}")
    args.creds = handle_credentials(args.creds)
    logger.info("Got credentials.")
    api = create_instance(args.creds)
    post_generator = get_posts(api, args)

    DB.connect(reuse_if_open=True)
    DB.create_tables([RedditPost, RedditComment], safe=True)
    logger.info("connected to database.")
    try:
        for reddit_data in post_generator:
            if reddit_data:
                append_db(reddit_data)
            else:
                break
    except KeyboardInterrupt:
        print("Exited.")
    print("Finished writing to database with all posts found")


if __name__ == "__main__":
    print("enter rdscp or reddit-scraper to run")
