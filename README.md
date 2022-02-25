# PyParaScraper

Pararius.nl scraper, based of the work done by [royreinders](https://github.com/royreinders/PyParascraper).

Features:

- Supports a couple, but not all, filters.
- Built-in anti-"bot detection" evasion 👺.
- Send new listings to telegram or discord.
- No hardcoded shizzels, everything is in a config file.

## Setup

1. Install the `requirements.txt`

`pip3 install requirements.txt`

2. Create copy of config.yml.example

`copy config.yml.example config.yml`

3. Setup the config file with your desired filters and telegram/discord info.

## Run

`python3 PyParascraper.py`
