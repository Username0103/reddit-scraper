import logging
from importlib.metadata import version
from pathlib import Path
from typing import Literal
from platformdirs import PlatformDirs

__version__ = version("reddit-scraper")

logger = logging.getLogger(__name__)

SORT_TYPE = Literal[
    "new",
    "hot",
    "top-all",
    "top-month",
    "top-week",
    "top-day",
    "top-hour",
    "controversial-all",
    "controversial-month",
    "controversial-week",
    "controversial-day",
    "controversial-hour",
]
DEFAULT_UA = "Scrapes reddit for SQL by Username0103. Programmed in Python, uses PRAW."
DATA_DIR = Path(PlatformDirs("reddit-scraper", "Username0103").user_data_dir)
CREDS_CACHE = DATA_DIR / "data.pkl"
