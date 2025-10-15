# Reddit Scraper

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-beta-yellow.svg)

Reddit Scraper is a Python-based tool designed to scrape posts and comments from Reddit and store them in a SQLite database. It leverages the PRAW (Python Reddit API Wrapper) library to interact with Reddit's API and Peewee ORM for database management. This tool is ideal for developers, researchers, or anyone interested in archiving Reddit data for analysis or other purposes.

## Features

- Scrape posts and comments from specified subreddits.
- Store data in a SQLite database for easy querying and analysis.
- Support for various sorting methods (e.g., hot, new, top, controversial) with time filters.
- Configurable options for skipping comments, setting post limits, and more.
- Credential caching to avoid repeated API key entry.
- Command-line interface for easy usage.

## Installation

### Prerequisites

- Python 3.10 or higher
- A Reddit API key (client ID and client secret). See [Reddit's API documentation](https://old.reddit.com/r/reddit.com/wiki/api) for instructions on obtaining one.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Username0103/AI-TUI.git
   cd AI-TUI
   ```

2. **Set Up a Virtual Environment** (optional but recommended)

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   Install the required Python packages listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install the Package**

   Install the Reddit Scraper package locally:

   ```bash
   pip install .
   ```

## Usage

Reddit Scraper can be run from the command line using either the `reddit-scraper` or `rdscp` command. Below are some common usage examples.

### Basic Usage

Scrape 20 hot posts from the `test` subreddit and store them in the database:

```bash
rdscp
```

### Advanced Usage

- **Scrape a Specific Number of Posts**

  Scrape 50 top posts from the past month in the `python` subreddit:

  ```bash
  rdscp -s python -n 50 -o top-month
  ```

- **Run Indefinitely**

  Scrape posts continuously until interrupted (Ctrl+C):

  ```bash
  rdscp -s python -n -1
  ```

- **Skip Comments**

  Scrape posts without their comments:

  ```bash
  rdscp -s python --skip-comments
  ```

- **Set Reddit API Credentials**

  Set your Reddit API credentials (only needs to be done once):

  ```bash
  rdscp --id YOUR_CLIENT_ID --key YOUR_CLIENT_SECRET
  ```

- **Clear Cached Credentials**

  Clear the cached credentials if you need to update them:

  ```bash
  rdscp -c
  ```

- **Change Sorting Method**

  Scrape controversial posts from the past week:

  ```bash
  rdscp -s python -o controversial-week
  ```

- **Debug Mode**

  Enable debug logging for (VERY) detailed output:

  ```bash
  rdscp -s python -vv
  ```

### Command-Line Options

Run `rdscp --help` to see all available options:

## Configuration

### Database

The scraped data is stored in a SQLite database named `reddit-scraper.db` in the current working directory. The database schema includes two main tables:

- `RedditPost`: Stores post metadata (e.g., title, author, score, etc.).
- `RedditComment`: Stores comment metadata, linked to posts via a foreign key.

### Credentials Cache

API credentials are cached in a file located at `~/.local/share/reddit-scraper/data.pkl` (or the equivalent directory on your operating system). Use the `-c` option to clear this cache if needed.
