import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import webbrowser
import pkg_resources
from typing import Dict, Optional

import httpx
from faker import Faker

from kurby.constants import DEFAULT_ACCEPT_LANGUAGE_HEADER, CHROME_HEADERS, PACKAGE_NAME

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
    # TODO: this is not reliable on all countries
    # try:
    #     local_settings, *_ = locale.getlocale()
    #     language_code, country_code = local_settings.split("_")
    #     return f"{language_code}-{country_code},{language_code};q=0.9"
    # except:
    return DEFAULT_ACCEPT_LANGUAGE_HEADER


def get_chrome_headers() -> Dict[str, str]:
    return {
        **CHROME_HEADERS,
        "accept-language": get_accept_language_header(),
        "user-agent": fake.chrome(),
    }


def get_current_version(package=PACKAGE_NAME) -> str:
    return pkg_resources.get_distribution(package).version


def check_for_update(current_version, package=PACKAGE_NAME) -> Optional[str]:
    try:
        r = httpx.get(f"https://pypi.org/pypi/{package}/json", timeout=1)
    except httpx.HTTPError:
        return
    releases = list(
        sorted(
            (
                {
                    "raw": k,
                    "version": tuple(int(x) for x in k.split("v", 1)[-1].split(".")),
                    "current": bool(k == current_version),
                }
                for k in r.json()["releases"]
            ),
            key=lambda r: r["version"],
            reverse=True,
        )
    )
    if releases and not releases[0]["current"]:
        return releases[0]["raw"]


def install_package(version, package=PACKAGE_NAME):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", f"{package}=={version}"]
    )
