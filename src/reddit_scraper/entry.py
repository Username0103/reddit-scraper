import argparse
import logging
import sys
from typing import get_args

from reddit_scraper import __version__, DEFAULT_UA, SORT_TYPE
from reddit_scraper import main


def parse_args(args) -> main.Options:
    parser = argparse.ArgumentParser(
        prog="rdscp",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"reddit-scraper {__version__}",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="loglevel",
        help="set loglevel to WARN",
        action="store_const",
        const=logging.WARN,
    )
    parser.add_argument(
        "-vv",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG, not recommended.",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-s",
        "--subreddit",
        dest="subreddit",
        default="test",
        help='select subreddit, does NOT include the leading the r/. defaults to "test"',
    )
    parser.add_argument(
        "-n",
        "--post-number",
        dest="num_posts",
        default=20,
        type=int,
        help="number of posts to archive. defaults to 20. set to -1 so it runs until you press ctrl-c",
    )
    sort_types = get_args(SORT_TYPE)
    parser.add_argument(
        "-o",
        "--sort",
        dest="sort_type",
        default="hot",
        choices=sort_types,
        help=f'type of sort to use on the selected sub. options are: "{'", "'.join(sort_types[:-1])}", or "{sort_types[-1]}".',
    )
    parser.add_argument(
        "-c",
        "--clear",
        dest="to_clear",
        default=False,
        action="store_true",
        help="clears your credentials cache",
    )
    parser.add_argument(
        "-k",
        "--skip-comments",
        dest="skip_comments",
        default=False,
        action="store_true",
        help="skips comments from posts",
    )
    parser.add_argument(
        "--id",
        dest="client_id",
        help="set your user agent. you only need to do this once. see https://old.reddit.com/r/reddit.com/wiki/api for getting one",
    )
    parser.add_argument(
        "--key",
        dest="api_key",
        help="set your api key. you only need to do this once. see https://old.reddit.com/r/reddit.com/wiki/api for getting one",
    )

    parser.add_argument(
        "--agent",
        dest="user_agent",
        default=DEFAULT_UA,
        help=f'set your user agent. defaults to "{DEFAULT_UA}".',
    )
    parsed_args = parser.parse_args(args)

    if not parsed_args.loglevel:
        parsed_args.loglevel = logging.INFO

    creds = main.RedditCredentials(
        client_id=parsed_args.client_id,
        api_key=parsed_args.api_key,
        user_agent=parsed_args.user_agent,
    )

    options = main.Options(
        loglevel=parsed_args.loglevel,
        subreddit=parsed_args.subreddit,
        num_posts=parsed_args.num_posts,
        to_clear=parsed_args.to_clear,
        sort_type=parsed_args.sort_type,
        skip_comments=parsed_args.skip_comments,
        creds=creds,
    )
    return options


def setup_logging(loglevel) -> None:
    logformat = "%(levelname)s: %(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat)


def enter_main(argses) -> None:
    args = parse_args(argses)
    setup_logging(args.loglevel)
    main.run(args)


def run() -> None:
    enter_main(sys.argv[1:])


if __name__ == "__main__":
    run()
