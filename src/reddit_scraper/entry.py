import argparse
import logging
import sys

from reddit_scraper import __version__
from . import main

def parse_args(args):
    parser = argparse.ArgumentParser()
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
    return parser.parse_args(args)


def setup_logging(loglevel):
    logformat = "%(levelname)s: %(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat
    )


def enter_main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    main.run()


def run():
    enter_main(sys.argv[1:])


if __name__ == "__main__":
    run()
