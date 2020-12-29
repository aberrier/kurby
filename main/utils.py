import os
import re
import tempfile
import unicodedata
import webbrowser

import httpx


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


def decrypt(message, key):
    from main.cryptojs import lib as cryptojs

    return cryptojs.AES.decrypt(message, key).toString(cryptojs.enc.Utf8)
