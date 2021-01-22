import httpx


class KurbyError(Exception):
    code = "undefined"
    message = "An unknown error occurred."

    def __init__(self):
        super().__init__(self.message)

    def __str__(self):
        return f"({self.code}): {self.message}"


class CrawlingError(KurbyError):
    code = "crawling_error"
    message = "An unknown crawling error occurred."


class SourceKeyError(CrawlingError):
    code = "source_key_error"
    message = "Couldn't get the source key."


class ServerError(CrawlingError):
    code = "server_error"
    message = "Twist didn't respond correctly. You might need to try again later."

    def __init__(self, exc: httpx.HTTPError):
        self.message += f"\n{exc.__cause__}"


class RequestError(CrawlingError):
    code = "request_error"
    message = "Something bad happened when requesting Twist. You might need update Kurby or to try again later."

    def __init__(self, exc: httpx.HTTPStatusError):
        self.message += f"\nError code {exc.response.status_code} while requesting {exc.request.url!r}."


class MissingEpisodeError(KurbyError):
    code = "missing_episode"
    message = "An episode is missing."

    def __init__(self, response: httpx.Response):
        self.response = response
