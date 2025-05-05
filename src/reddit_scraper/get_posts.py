from __future__ import annotations

from dataclasses import dataclass
import sys
from typing import TYPE_CHECKING, Any, Generator, Iterator
import math
from datetime import datetime

import praw
from praw.models import Comment, Submission
from praw.models.comment_forest import CommentForest
from prawcore import Forbidden

from reddit_scraper import logger
from .database import RedditPost

if TYPE_CHECKING:
    from .get_credentials import RedditCredentials
    from .main import Options


def create_instance(creds: RedditCredentials) -> praw.Reddit:
    return praw.Reddit(
        client_id=creds.client_id,
        client_secret=creds.api_key,
        user_agent=creds.user_agent,
    )


def get_comment_data(post: Submission) -> list[dict[str, Any]]:
    post.comments.replace_more(limit=None)
    comments_list = post.comments.list()
    return format_comments(comments_list)  # type: ignore


def format_comments(
    comments_list: list[Comment] | CommentForest,
) -> list[dict[str, Any]]:
    serialized = []
    for comment in comments_list:
        if isinstance(comment, CommentForest):
            logger.info(f"skipped comment {comment.id}")
            continue
        serialized.append(
            {
                "name": comment.name,
                "author": str(comment.author),
                "body": comment.body,
                "created_utc": datetime.fromtimestamp(comment.created_utc),
                "distinguished": comment.distinguished,
                "edited": comment.edited,
                "parent_id": comment.parent_id,
                "replies": format_comments(comment.replies) if comment.replies else [],
                "saved": comment.saved,
                "score": comment.score,
                "stickied": comment.stickied,
                "submission": str(comment.submission),
                "subreddit": str(comment.subreddit),
                "depth": comment.depth,
            }
        )
    return serialized


def get_post_data(post: Submission) -> dict:
    author = str(post.author)
    return {
        "author": author if author != "None" else None,
        "created_utc": datetime.fromtimestamp(post.created_utc),
        "distinguished": post.distinguished,
        "edited": post.edited,
        "locked": post.locked,
        "name": post.name,
        "num_comments": post.num_comments,
        "over_18": post.over_18,
        "score": post.score,
        "is_textual": post.is_self,
        "selftext": post.selftext,
        "spoiler": post.spoiler,
        "subreddit": str(post.subreddit),
        "title": post.title,
        "upvote_ratio": post.upvote_ratio,
    }


@dataclass
class RedditData:
    post: dict
    comments: list[dict] | None


def get_db_ids() -> list[str]:
    if RedditPost.table_exists():
        ids = RedditPost.select(RedditPost.name).scalars()
        return list(ids)
    return []

def make_sort(api: praw.Reddit, options: Options) -> Iterator[Submission]:
    sort = options.sort_type
    sub = api.subreddit(options.subreddit)
    sort_time = sort.rsplit("-", maxsplit=1)[-1]
    sort_name = sort.split("-", maxsplit=1)[0]
    if sort_name in {"top", "controversial"}:
        return getattr(sub, sort_name)(time_filter=sort_time)
    return getattr(sub, sort_name)()


def get_posts(api: praw.Reddit, options: Options) -> Generator[Any, None, None]:
    max_posts = options.num_posts if options.num_posts != -1 else math.inf
    posts = make_sort(api, options)
    i = 0
    ids = get_db_ids()
    try:
        for post in posts:
            if not post.stickied or post.num_comments < 50 or options.skip_comments:
                if post.name not in ids:
                    i += 1
                    if i > max_posts:
                        break
                    ids.append(post.name)
                    logger.info(f"Found post: {post.name} on r/{str(post.subreddit)}")

                    if not options.skip_comments:
                        comment_data = get_comment_data(post)
                    else:
                        comment_data = None

                    yield RedditData(get_post_data(post), comment_data)
                else:
                    logger.info(f"Skipped post: {post.name} on r/{str(post.subreddit)} due to already being archived")
            else:
                logger.info(f"Skipped post: {post.name} on r/{str(post.subreddit)} due to being stickied post with tons of comments")
    except Forbidden:
        logger.error("Recieved 403 forbidden response. Double check your API key and create a new reddit application if nothing else works. Make sure to select the script type of application.")
        sys.exit(1)
