import re
from typing import List
from urllib.parse import urljoin

import httpx
import js2py
from faker import Faker
from pydantic import parse_obj_as

from kurby.constants import TWIST_URL, ANIME_ENDPOINT
from kurby.decrypt import decrypt
from kurby.schemas import Anime, AnimeDetails, AnimeSource
from kurby.utils import get_chrome_headers

fake = Faker()


class TwistClient(httpx.Client):
    source_key = None
    access_token = None


def get_auth_client() -> TwistClient:
    headers = get_chrome_headers()
    r = httpx.get(url=TWIST_URL, headers=headers)
    r.raise_for_status()
    match = re.search(r"<script>(.*)<\/script>", r.content.decode("utf-8"))
    script = match.group(1)
    script = script.replace("=eval", "=function(a) {return a;}")
    cookie_script = js2py.eval_js(script).replace("location.reload();", "")
    cookie_script = cookie_script.replace("document.cookie=", "value=")
    cookie_script += "func=function(a) {return a;};func(value);"
    cookie = js2py.eval_js(cookie_script).split("=", 1)
    cookies = {cookie[0]: cookie[1]}

    r = httpx.get(url=TWIST_URL, headers=headers, cookies=cookies)
    match = re.search(
        r'<script src="(\/_nuxt\/\w+\.js)" type="text\/javascript"><\/script>\s*$',
        r.content.decode("utf-8"),
    )
    script_url = urljoin(TWIST_URL, match.group(1))
    r = httpx.get(url=urljoin(TWIST_URL, script_url), headers=headers, cookies=cookies)
    content = r.content.decode("utf-8")
    r.raise_for_status()
    match = re.search(r'"x-access-token":"([\w]+)"', content)
    access_token = match.group(1)
    c = TwistClient(
        headers={**headers, "x-access-token": access_token}, cookies=cookies
    )
    # Extra parameters
    match = re.search(r',k:"(.+)",mount', content)
    c.source_key = match.group(1)
    c.access_token = access_token
    return c


client = get_auth_client()


def get_animes() -> List[Anime]:
    with client:
        r = client.get(url=f"{TWIST_URL}{ANIME_ENDPOINT}")
        r.raise_for_status()
        return parse_obj_as(List[Anime], r.json())


def get_anime_details(anime: Anime) -> AnimeDetails:
    with client:
        url = f"{TWIST_URL}{ANIME_ENDPOINT}/{anime.slug.slug}"
        r = client.get(url=url)
        r.raise_for_status()
        anime_details: AnimeDetails = AnimeDetails.parse_obj(r.json())
        return anime_details


def get_sources(anime: Anime) -> List[AnimeSource]:
    with client:
        source_key = client.source_key
        url = f"{TWIST_URL}{ANIME_ENDPOINT}/{anime.slug.slug}/sources"
        r = client.get(url=url)
        r.raise_for_status()
        sources: List[AnimeSource] = parse_obj_as(List[AnimeSource], r.json())
        # Decrypt and complete source
        for source in sources:
            source.source = (
                decrypt(source.source.encode("utf-8"), source_key.encode("utf-8"))
                .decode("utf-8")
                .replace(" ", "%20")
            )
        return sources
