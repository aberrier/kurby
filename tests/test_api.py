import random
from urllib.parse import urljoin

import httpx
import pytest
from httpx import HTTPStatusError

from kurby.api import get_auth_client, get_animes, get_anime_details, get_sources
from kurby.constants import TWIST_CDN_URL, TWIST_URL


@pytest.mark.external
@pytest.mark.enable_socket
class TestAPI:
    def test_auth_client(self):
        client = get_auth_client()
        assert client.source_key is not None
        assert client.access_token is not None

    def test_get_animes(self):
        animes = get_animes()
        assert len(animes) > 1000
        naruto_anime = list(filter(lambda a: a.slug.slug == "naruto", animes))[0]
        assert naruto_anime.title == "Naruto"
        assert naruto_anime.id == 451

    def test_get_anime_details(self, anime):
        anime_details = get_anime_details(anime)
        assert anime_details.title == "Naruto"
        assert "Konoha" in anime_details.description
        assert len(anime_details.episodes) == 209

    def test_get_sources(self, anime):
        sources = get_sources(anime)
        assert len(sources) == 209
        assert sources[0].source == "/anime/narutoold/naruto-001.mp4"

    def test_check_sources_random(self):
        iterations = 0
        animes = get_animes()
        while iterations <= 100:
            iterations += 1
            random_anime = random.choice(animes)
            current_sources = get_sources(random_anime)
            if current_sources:
                source = random.choice(current_sources)
                url = urljoin(TWIST_CDN_URL, source.source)
                client = get_auth_client()
                try:
                    r = client.get(
                        url,
                        headers={
                            **dict(client.headers),
                            "referer": TWIST_URL,
                            "range": "bytes=0-10",
                        },
                    )
                    r.raise_for_status()
                except httpx.HTTPError as e:
                    print(
                        f"Error on iteration n°{iterations} for {random_anime.full_title()}\n\tepisode={source.number}"
                        f"{e}\n"
                    )
                    continue
                print(
                    f"Found source for {random_anime.full_title()}\n\tepisode={source.number}\n\turl={r.url}"
                )
                break
        assert iterations <= 100
