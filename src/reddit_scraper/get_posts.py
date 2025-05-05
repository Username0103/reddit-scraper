from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generator
import math
from datetime import datetime

import praw
from praw.models import Comment, Submission
from praw.models.comment_forest import CommentForest

from reddit_scraper import logger

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
            logger.debug(f"skipped comment {comment.id}")
            continue
        serialized.append(
            {
                "name": comment.name,
                "author": str(comment.author),
                "body": comment.body,
                "created_utc": datetime.fromtimestamp(comment.created_utc),
                "distinguished": comment.distinguished,
                "edited": comment.edited,
                "reddit_id": comment.id,
                "is_submitter": comment.is_submitter,
                "link_id": comment.link_id,
                "parent_id": comment.parent_id,
                "permalink": comment.permalink,
                "replies": format_comments(comment.replies) if comment.replies else [],
                "saved": comment.saved,
                "score": comment.score,
                "stickied": comment.stickied,
                "submission": str(comment.submission),
                "subreddit": str(comment.subreddit),
                "subreddit_id": comment.subreddit_id,
                "depth": comment.depth,
            }
        )
    return serialized


def get_post_data(post: Submission) -> dict:
    return {
        "author": str(post.author),
        "author_flair_text": post.author_flair_text,
        "created_utc": datetime.fromtimestamp(post.created_utc),
        "distinguished": post.distinguished,
        "edited": post.edited,
        "reddit_id": post.name,
        "is_original_content": post.is_original_content,
        "is_self": post.is_self,
        "link_flair_template_id": post.author_flair_template_id,
        "link_flair_text": post.link_flair_text,
        "locked": post.locked,
        "name": post.name,
        "num_comments": post.num_comments,
        "over_18": post.over_18,
        "permalink": post.permalink,
        "saved": post.saved,
        "score": post.score,
        "selftext": post.selftext,
        "spoiler": post.spoiler,
        "stickied": post.stickied,
        "subreddit": str(post.subreddit),
        "title": post.title,
        "upvote_ratio": post.upvote_ratio,
        "url": post.url,
    }


@dataclass
class RedditData:
    post: dict
    comments: list[dict] | None


def get_posts(api: praw.Reddit, options: Options) -> Generator[Any, None, None]:
    max_posts = options.num_posts if options.num_posts != -1 else math.inf
    posts = api.subreddit(options.subreddit).hot()
    i = 0
    for post in posts:
        i += 1
        if i > max_posts:
            break
        logger.info(f"Found post: {post.id} on r/{str(post.subreddit)}")

        if not options.skip_comments:
            comment_data = get_comment_data(post)
        else:
            comment_data = None

        yield RedditData(get_post_data(post), comment_data)
