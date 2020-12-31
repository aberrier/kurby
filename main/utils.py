import os
import re
import tempfile
import unicodedata
import webbrowser
import locale
from typing import Dict

import httpx
from faker import Faker

from main.constants import DEFAULT_ACCEPT_LANGUAGE_HEADER, CHROME_HEADERS

fake = Faker()


def open_in_browser(response: httpx.Response):
    content = response.content

    if b"<base" not in content:
        repl = f'<head><base href="{response.url}">'.encode("utf-8")
        content = content.replace(b"<head>", repl)
    ext = ".html"
    fd, fname = tempfile.mkstemp(ext)
    os.write(fd, content)
    os.close(fd)
    return webbrowser.open("file://%s" % fname)


def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s]", ".", value).strip()
    return "".join(
        x for x in re.sub(r"[\.\s]+", ".", value) if x.isalnum() or x in "._- "
    )


def get_accept_language_header() -> str:
    try:
        local_settings, *_ = locale.getlocale()
        language_code, country_code = local_settings.split("_")
        return f"{language_code}-{country_code},{language_code};q=0.9"
    except:
        return DEFAULT_ACCEPT_LANGUAGE_HEADER


def get_chrome_headers() -> Dict[str, str]:
    return {
        **CHROME_HEADERS,
        "accept-language": get_accept_language_header(),
        "user-agent": fake.chrome(),
    }
