import base64
import re
from typing import List
from urllib.parse import urljoin

import httpx
import js2py
from pydantic import parse_obj_as

from kurby.constants import TWIST_URL, ANIME_ENDPOINT, DEFAULT_TIMEOUT
from kurby.decrypt import decrypt
from kurby.exceptions import SourceKeyError, ServerError, RequestError
from kurby.schemas import Anime, AnimeDetails, AnimeSource
from kurby.utils import get_chrome_headers


class TwistClient(httpx.Client):
    source_key = None
    access_token = None


def get_source_key(content: str) -> bytes:
    match = re.search(r',k:.*\("(.*?)"\),mount', content)
    if not match:
        raise SourceKeyError
    return base64.b64decode(match.group(1))


def get_auth_client() -> TwistClient:
    headers = get_chrome_headers()
    try:
        r = httpx.get(url=TWIST_URL, headers=headers, timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
        match = re.search(r"<script>(.*)<\/script>", r.content.decode("utf-8"))
        script = match.group(1)
        script = script.replace("=eval", "=function(a) {return a;}")
        cookie_script = js2py.eval_js(script).replace("location.reload();", "")
        cookie_script = cookie_script.replace("document.cookie=", "value=")
        cookie_script += "func=function(a) {return a;};func(value);"
        cookie = js2py.eval_js(cookie_script).split("=", 1)
        cookies = {cookie[0]: cookie[1]}

        r = httpx.get(
            url=TWIST_URL, headers=headers, cookies=cookies, timeout=DEFAULT_TIMEOUT
        )
        match = re.search(
            r'<script src="(\/_nuxt\/\w+\.js)" type="text\/javascript"><\/script>\s*$',
            r.content.decode("utf-8"),
        )
        script_url = urljoin(TWIST_URL, match.group(1))
        r = httpx.get(
            url=urljoin(TWIST_URL, script_url),
            headers=headers,
            cookies=cookies,
            timeout=DEFAULT_TIMEOUT,
        )
        content = r.content.decode("utf-8")
        r.raise_for_status()
        match = re.search(r'"x-access-token":"([\w]+)"', content)
        access_token = match.group(1)
    except httpx.HTTPStatusError as e:
        raise RequestError(e)
    except httpx.HTTPError as e:
        raise ServerError(e)

    c = TwistClient(
        headers={**headers, "x-access-token": access_token},
        cookies=cookies,
        timeout=DEFAULT_TIMEOUT,
    )
    # Extra parameters
    c.source_key = get_source_key(content)
    c.access_token = access_token
    return c


def get_animes() -> List[Anime]:
    with get_auth_client() as client:
        try:
            r = client.get(url=f"{TWIST_URL}{ANIME_ENDPOINT}")
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise RequestError(e)
        except httpx.HTTPError as e:
            raise ServerError(e)
        return parse_obj_as(List[Anime], r.json())


def get_anime_details(anime: Anime) -> AnimeDetails:
    with get_auth_client() as client:
        url = f"{TWIST_URL}{ANIME_ENDPOINT}/{anime.slug.slug}"
        try:
            r = client.get(url=url)
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise RequestError(e)
        except httpx.HTTPError as e:
            raise ServerError(e)

        anime_details: AnimeDetails = AnimeDetails.parse_obj(r.json())
        return anime_details


def get_sources(anime: Anime) -> List[AnimeSource]:
    with get_auth_client() as client:
        source_key = client.source_key
        url = f"{TWIST_URL}{ANIME_ENDPOINT}/{anime.slug.slug}/sources"
        try:
            r = client.get(url=url)
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise RequestError(e)
        except httpx.HTTPError as e:
            raise ServerError(e)
        sources: List[AnimeSource] = parse_obj_as(List[AnimeSource], r.json())
        # Decrypt and complete source
        for source in sources:
            source.source = (
                decrypt(source.source.encode("utf-8"), source_key)
                .decode("utf-8")
                .replace(" ", "%20")
            )
        return sources
