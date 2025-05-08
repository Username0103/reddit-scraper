from __future__ import annotations

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)
from playhouse.sqlite_ext import SqliteExtDatabase

from typing import TYPE_CHECKING
from reddit_scraper import logger

if TYPE_CHECKING:
    from .get_posts import RedditData


def make_db() -> SqliteExtDatabase:
    db = SqliteExtDatabase(
        "reddit-scraper.db",
        pragmas=(
            ("cache_size", -1024 * 64),
            ("journal_mode", "wal"),
            ("foreign_keys", 1),
        ),
    )
    return db


DB = make_db()


class BaseModel(Model):
    name = CharField()

    class Meta:
        database = DB


class RedditContent(BaseModel):
    name = CharField(primary_key=True, unique=True, max_length=15)
    author = TextField(null=True)
    created_utc = DateTimeField()
    distinguished = TextField(null=True)
    edited = BooleanField()
    score = IntegerField(default=0)
    subreddit = TextField()


class RedditPost(RedditContent):
    locked = BooleanField()
    num_comments = IntegerField(default=0)
    over_18 = BooleanField()
    selftext = TextField(null=True)
    is_textual = BooleanField(default=False)
    spoiler = BooleanField()
    title = TextField()
    img_link_or_permalink = TextField()
    upvote_ratio = FloatField(null=True)


class RedditComment(RedditContent):
    post = ForeignKeyField(RedditPost, backref="comments", field=RedditPost.name)
    parent_id = CharField(null=True, max_length=15, index=True)
    body = TextField(null=True)
    saved = BooleanField(default=False)
    stickied = BooleanField(default=False)
    depth = IntegerField()


def append_db(data: RedditData) -> None:
    try:
        with DB.atomic():
            logger.debug(f"saving post: {data.post.get('name', '?')}")
            RedditPost.insert(data.post).on_conflict_replace().execute()
            if data.comments:
                append_comments(data.comments, data.post["name"])
    except Exception as e:
        logger.error(
            f"database post saving error! {data.post['name']}: error {e}",
            exc_info=True,
        )


def append_comments(comments: list[dict], post_id: str) -> None:
    to_save: list[dict] = []
    to_recurse = []

    for comment_data in comments:
        replies = comment_data.get("replies", [])
        comment_data["post"] = post_id
        if replies:
            to_recurse.extend(replies)
        no_replies = {
            k: v for k, v in comment_data.items() if k not in {"replies", "submission"}
        }
        to_save.append(no_replies)

    if to_save:
        try:
            for comment in to_save:
                logger.debug(f"saving comments: {comment.get('name', '???')}")
                RedditComment.insert(comment).on_conflict_replace().execute()
        except Exception as e:
            logger.error(
                f"database comment saving error! {post_id}: error {e}",
                exc_info=True,
            )

    if to_recurse:
        append_comments(to_recurse, post_id)
