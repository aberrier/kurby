import os
from pathlib import Path

# API
import typer

TWIST_URL = "https://twist.moe"
TWIST_CDN_URL = "https://twistcdn.bunny.sh"
ANIME_ENDPOINT = "/api/anime"


DEFAULT_ACCEPT_LANGUAGE_HEADER = "en-US,en;q=0.9"
CHROME_HEADERS = {
    "authority": "twist.moe",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    "sec-ch-ua-mobile": "?0",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
}
# CLI
ANIMES_COMMAND_NAME = "animes"
DETAILS_COMMAND_NAME = "details"
DOWNLOAD_COMMAND_NAME = "download"
UPDATE_COMMAND_NAME = "update"

ANIME_SLUG_HELP = (
    "Anime slug. Use "
    + typer.style(ANIMES_COMMAND_NAME, bold=True)
    + " command for more information."
)
TWIST_SUPPORTING_MESSAGE = (
    "If you are using Kurby, please consider donating to "
    + typer.style("https://twist.moe/", fg=typer.colors.BLUE, bold=True)
    + " and supporting the project on Github !\n"
)

# MISC
PACKAGE_NAME = "kurby"
CWD_DIR = Path(os.getcwd())
ROOT_DIR = os.path.dirname(Path(__file__).parent)
FUZZY_SEARCH_THRESHOLD = 60
FUZZY_SEARCH_MAX_RESULTS = 10
