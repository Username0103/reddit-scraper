import argparse
import logging
import sys

from reddit_scraper import __version__, DEFAULT_UA
from reddit_scraper import main


def parse_args(args) -> main.Options:
    parser = argparse.ArgumentParser(
        prog="rdscp",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"reddit-scraper {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-s",
        "--subreddit",
        dest="subreddit",
        default="all",
        help='select subreddit, does NOT include the leading the r/. defaults to "all"',
    )
    parser.add_argument(
        "-n",
        "--post-number",
        dest="num_posts",
        default=5,
        type=int,
        help="number of posts to archive. defaults to 5. set to -1 so it runs until you press ctrl-c",
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
        dest="to_skip",
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
        skip_comments=parsed_args.to_skip,
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
