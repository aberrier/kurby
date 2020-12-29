import os
from pathlib import Path

# API
import typer

TWIST_URL = "https://twist.moe"
ANIME_ENDPOINT = "/api/anime"
ONGOING_FILES_URL = "https://hot-paw-03.cdn.bunny.sh"
FILES_URL = "https://edge-6.cdn.bunny.sh"

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
    "accept-language": "fr-FR,fr;q=0.9",
}
# CLI
ANIME_SLUG_HELP = (
    "Anime slug. Use "
    + typer.style("animes", bold=True)
    + " command for more information."
)

# MISC
ROOT_DIR = os.path.dirname(Path(__file__).parent)
FUZZY_SEARCH_THRESHOLD = 60
FUZZY_SEARCH_MAX_RESULTS = 10
