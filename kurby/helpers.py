import logging
import warnings
from pathlib import Path
from typing import List, Optional, Dict, Union
from urllib.parse import urljoin

import httpcore
import httpx
import typer
from PyInquirer import prompt
from tenacity import (
    retry,
    before_sleep_log,
    retry_if_exception_type,
    wait_fixed,
    wait_random,
)
from tqdm import tqdm

from kurby.api import get_auth_client, get_animes
from kurby.constants import (
    FUZZY_SEARCH_THRESHOLD,
    FUZZY_SEARCH_MAX_RESULTS,
    TWIST_CDN_URL,
)
from kurby.constants import TWIST_URL
from kurby.schemas import Anime, AnimeSource

warnings.simplefilter("ignore")
from fuzzywuzzy import fuzz

logger = logging.getLogger(__name__)


def filter_animes(
    search: str,
    animes: Optional[List[Anime]] = None,
    threshold: int = FUZZY_SEARCH_THRESHOLD,
    limit: int = FUZZY_SEARCH_MAX_RESULTS,
):
    if animes is None:
        animes = get_animes()
    animes_by_title = dict(
        sorted(((anime.title, anime) for anime in animes), key=lambda x: x[0])
    )
    animes_by_alt_title = dict(
        sorted(
            ((anime.alt_title, anime) for anime in animes if anime.alt_title),
            key=lambda x: x[0],
        )
    )
    selected_animes_with_score_by_id = {}
    for anime in animes_by_title.values():
        score = fuzz.token_set_ratio(search.lower(), anime.title.lower())
        if score > threshold:
            selected_animes_with_score_by_id[anime.id] = (score, anime)
    for anime in animes_by_alt_title.values():
        score = fuzz.token_set_ratio(search.lower(), anime.alt_title.lower())
        if score > threshold:
            selected_animes_with_score_by_id[anime.id] = (score, anime)
    return list(
        x[1]
        for x in sorted(
            selected_animes_with_score_by_id.values(),
            key=lambda x: x[0],
            reverse=True,
        )
    )[:limit]


@retry(
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.ERROR),
    retry=retry_if_exception_type(httpcore.TimeoutException)
    | retry_if_exception_type(httpx.NetworkError)
    | retry_if_exception_type(httpx.TransportError)
    | retry_if_exception_type(httpx.HTTPStatusError),
    wait=wait_fixed(2) + wait_random(1, 10),
)
def download_source(source: AnimeSource, filepath: Path):
    with get_auth_client() as new_client:
        url = urljoin(TWIST_CDN_URL, source.source)
        with new_client.stream(
            "GET",
            url,
            headers={**dict(new_client.headers), "referer": TWIST_URL},
        ) as response:
            if response.status_code == 404:
                typer.secho(
                    f"Couldn't find the episode ({url}). Skipping...",
                    fg=typer.colors.RED,
                    bold=True,
                )
                return
            response.raise_for_status()
            total = int(response.headers.get("Content-Length"))
            with filepath.open("wb") as file:
                with tqdm(
                    total=total, unit_scale=True, unit_divisor=1024, unit="B"
                ) as progress:
                    num_bytes_downloaded = response.num_bytes_downloaded
                    for chunk in response.iter_bytes():
                        file.write(chunk)
                        progress.update(
                            response.num_bytes_downloaded - num_bytes_downloaded
                        )
                        num_bytes_downloaded = response.num_bytes_downloaded


def select_anime_slug(slug: Optional[str]) -> str:
    def get_choices(context: Dict[str, str]) -> List[Dict[str, Union[str, Anime]]]:
        animes = get_animes()
        if context.get("filter"):
            animes = filter_animes(context["filter"], animes=animes)
        return [
            {"name": anime.full_title(), "value": anime}
            for anime in sorted((a for a in animes), key=lambda a: a.title)
        ]

    if slug is None:
        questions = [
            {
                "type": "input",
                "name": "filter",
                "message": "Apply a filter (Press [ENTER] to ignore):",
            },
            {
                "type": "list",
                "name": "anime",
                "message": "Select an anime:",
                "choices": get_choices,
            },
        ]
        answers = prompt(questions)
        if "anime" not in answers:
            raise typer.BadParameter(f"No choice selected.")
        return answers["anime"].slug.slug
    return slug
