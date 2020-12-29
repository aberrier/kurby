import re
from urllib.parse import urljoin
from faker import Faker
import httpx
import js2py

from main.constants import TWIST_URL, CHROME_HEADERS

fake = Faker()


def get_auth_client() -> httpx.Client:
    headers = CHROME_HEADERS | {"user-agent": fake.chrome()}
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
    c = httpx.Client(
        headers=headers | {"x-access-token": access_token}, cookies=cookies
    )
    # Extra parameters
    match = re.search(r',k:"(.+)",mount', content)
    c.source_key = match.group(1)
    return c


client = get_auth_client()
