import datetime
from contextlib import contextmanager

import pytest
from typer.testing import CliRunner
import typer

from kurby.schemas import Anime, AnimeSlug, AnimeDetails, AnimeEpisode, AnimeSource


@contextmanager
def monkeysessioncontext():
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope="session")
def monkeysession(request):
    with monkeysessioncontext() as mp:
        return mp


@pytest.fixture()
def no_styling(monkeypatch, pytestconfig):
    monkeypatch.setattr(typer, "style", lambda text, *a, **k: text)
    monkeypatch.setattr(typer, "secho", lambda message, *a, **k: typer.echo(message))


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture()
def naruto_animes():
    return [
        Anime(
            id=810,
            title="Boruto: Naruto Next Generations",
            alt_title=None,
            season=0,
            ongoing=1,
            hb_id=13051,
            created_at=datetime.datetime(2017, 4, 5, 17, 13, 20),
            updated_at=datetime.datetime(2020, 10, 25, 15, 42, 35),
            hidden=False,
            mal_id=34566,
            slug=AnimeSlug(
                id=1045,
                slug="boruto-naruto-next-generations",
                anime_id=810,
                created_at=datetime.datetime(2017, 4, 5, 17, 13, 20),
                updated_at=datetime.datetime(2017, 4, 5, 17, 13, 20),
            ),
        ),
        Anime(
            id=451,
            title="Naruto",
            alt_title=None,
            season=1,
            ongoing=0,
            hb_id=11,
            created_at=datetime.datetime(2016, 8, 12, 0, 58, 22),
            updated_at=datetime.datetime(2020, 9, 10, 22, 58, 27),
            hidden=False,
            mal_id=20,
            slug=AnimeSlug(
                id=452,
                slug="naruto",
                anime_id=451,
                created_at=datetime.datetime(2016, 8, 12, 0, 58, 23),
                updated_at=datetime.datetime(2016, 8, 12, 0, 58, 23),
            ),
        ),
        Anime(
            id=639,
            title="Naruto: Shippuuden",
            alt_title="Naruto: Shippuden",
            season=2,
            ongoing=0,
            hb_id=1555,
            created_at=datetime.datetime(2016, 8, 22, 14, 46, 28),
            updated_at=datetime.datetime(2020, 9, 10, 22, 58, 33),
            hidden=False,
            mal_id=1735,
            slug=AnimeSlug(
                id=2315,
                slug="naruto-shippuuden",
                anime_id=639,
                created_at=datetime.datetime(2020, 2, 27, 15, 5, 9),
                updated_at=datetime.datetime(2020, 2, 27, 15, 5, 9),
            ),
        ),
        Anime(
            id=1517,
            title="The Last: Naruto the Movie",
            alt_title=None,
            season=0,
            ongoing=0,
            hb_id=7543,
            created_at=datetime.datetime(2019, 3, 8, 13, 49, 43),
            updated_at=datetime.datetime(2020, 9, 11, 0, 2, 46),
            hidden=False,
            mal_id=16870,
            slug=AnimeSlug(
                id=1975,
                slug="the-last-naruto-the-movie",
                anime_id=1517,
                created_at=datetime.datetime(2019, 3, 8, 13, 49, 43),
                updated_at=datetime.datetime(2019, 3, 8, 13, 49, 43),
            ),
        ),
    ]


@pytest.fixture()
def one_piece_animes():
    return [
        Anime(
            id=638,
            title="One Piece",
            alt_title=None,
            season=1,
            ongoing=1,
            hb_id=12,
            created_at=datetime.datetime(2016, 8, 22, 14, 4, 7),
            updated_at=datetime.datetime(2020, 10, 25, 15, 46, 7),
            hidden=False,
            mal_id=21,
            slug=AnimeSlug(
                id=845,
                slug="one-piece",
                anime_id=638,
                created_at=datetime.datetime(2016, 8, 22, 14, 4, 7),
                updated_at=datetime.datetime(2016, 8, 22, 14, 4, 7),
            ),
        ),
        Anime(
            id=1423,
            title="One Piece: Heart of Gold",
            alt_title=None,
            season=0,
            ongoing=0,
            hb_id=12228,
            created_at=datetime.datetime(2019, 1, 21, 21, 46, 13),
            updated_at=datetime.datetime(2020, 8, 25, 14, 49, 40),
            hidden=True,
            mal_id=33338,
            slug=AnimeSlug(
                id=1844,
                slug="one-piece-heart-of-gold",
                anime_id=1423,
                created_at=datetime.datetime(2019, 1, 21, 21, 46, 13),
                updated_at=datetime.datetime(2019, 1, 21, 21, 46, 13),
            ),
        ),
    ]


@pytest.fixture()
def one_punch_animes():
    return [
        Anime(
            id=616,
            title="One Punch Man",
            alt_title=None,
            season=1,
            ongoing=0,
            hb_id=10740,
            created_at=datetime.datetime(2016, 8, 13, 1, 16, 22),
            updated_at=datetime.datetime(2020, 8, 17, 19, 11, 20),
            hidden=False,
            mal_id=None,
            slug=AnimeSlug(
                id=621,
                slug="one-punch-man",
                anime_id=616,
                created_at=datetime.datetime(2016, 8, 13, 1, 16, 22),
                updated_at=datetime.datetime(2016, 8, 13, 1, 16, 22),
            ),
        ),
        Anime(
            id=1551,
            title="One Punch Man 2",
            alt_title=None,
            season=2,
            ongoing=0,
            hb_id=12566,
            created_at=datetime.datetime(2019, 4, 9, 22, 6, 3),
            updated_at=datetime.datetime(2020, 8, 17, 19, 11, 29),
            hidden=False,
            mal_id=34134,
            slug=AnimeSlug(
                id=2014,
                slug="one-punch-man-2",
                anime_id=1551,
                created_at=datetime.datetime(2019, 4, 9, 22, 6, 3),
                updated_at=datetime.datetime(2019, 4, 9, 22, 6, 3),
            ),
        ),
    ]


@pytest.fixture()
def attack_on_titan_animes():
    return [
        Anime(
            id=230,
            title="Shingeki no Kyojin",
            alt_title="Attack on Titan",
            season=1,
            ongoing=0,
            hb_id=7442,
            created_at=datetime.datetime(2016, 8, 12, 0, 57, 1),
            updated_at=datetime.datetime(2020, 8, 17, 19, 6, 21),
            hidden=False,
            mal_id=16498,
            slug=AnimeSlug(
                id=657,
                slug="shingeki-no-kyojin",
                anime_id=230,
                created_at=datetime.datetime(2016, 8, 14, 12, 50, 6),
                updated_at=datetime.datetime(2016, 8, 14, 12, 50, 6),
            ),
        ),
        Anime(
            id=801,
            title="Shingeki no Kyojin Season 2",
            alt_title="Attack on Titan Season 2",
            season=2,
            ongoing=0,
            hb_id=8671,
            created_at=datetime.datetime(2017, 4, 1, 20, 59, 42),
            updated_at=datetime.datetime(2020, 8, 17, 19, 6, 29),
            hidden=False,
            mal_id=25777,
            slug=AnimeSlug(
                id=1019,
                slug="shingeki-no-kyojin-season-2",
                anime_id=801,
                created_at=datetime.datetime(2017, 4, 1, 20, 59, 42),
                updated_at=datetime.datetime(2017, 4, 1, 20, 59, 42),
            ),
        ),
        Anime(
            id=1222,
            title="Shingeki no Kyojin Season 3",
            alt_title="Attack on Titan Season 3",
            season=3,
            ongoing=0,
            hb_id=13569,
            created_at=datetime.datetime(2018, 7, 22, 23, 20),
            updated_at=datetime.datetime(2020, 8, 17, 19, 6, 34),
            hidden=False,
            mal_id=35760,
            slug=AnimeSlug(
                id=1508,
                slug="shingeki-no-kyojin-season-3",
                anime_id=1222,
                created_at=datetime.datetime(2018, 7, 22, 23, 20),
                updated_at=datetime.datetime(2018, 7, 22, 23, 20),
            ),
        ),
        Anime(
            id=2158,
            title="Shingeki no Kyojin The Final Season",
            alt_title="Attack on Titan The Final Season",
            season=4,
            ongoing=1,
            hb_id=42422,
            created_at=datetime.datetime(2020, 12, 6, 16, 2, 58),
            updated_at=datetime.datetime(2020, 12, 6, 23, 6, 16),
            hidden=False,
            mal_id=40028,
            slug=AnimeSlug(
                id=2783,
                slug="shingeki-no-kyojin-the-final-season",
                anime_id=2158,
                created_at=datetime.datetime(2020, 12, 6, 16, 2, 58),
                updated_at=datetime.datetime(2020, 12, 6, 16, 2, 58),
            ),
        ),
    ]


@pytest.fixture()
def animes(naruto_animes, one_piece_animes, one_punch_animes, attack_on_titan_animes):
    return naruto_animes + one_punch_animes + one_piece_animes + attack_on_titan_animes


@pytest.fixture()
def anime():
    return Anime(
        id=451,
        title="Naruto",
        alt_title=None,
        season=1,
        ongoing=0,
        hb_id=11,
        created_at=datetime.datetime(2016, 8, 12, 0, 58, 22),
        updated_at=datetime.datetime(2020, 9, 10, 22, 58, 27),
        hidden=False,
        mal_id=20,
        slug=AnimeSlug(
            id=452,
            slug="naruto",
            anime_id=451,
            created_at=datetime.datetime(2016, 8, 12, 0, 58, 23),
            updated_at=datetime.datetime(2016, 8, 12, 0, 58, 23),
        ),
    )


@pytest.fixture()
def anime_details(anime):
    return AnimeDetails(
        **anime.dict(),
        description="Toto le rigolo",
        episodes=[
            AnimeEpisode.parse_obj(
                {
                    **anime.dict(),
                    "id": 8101 + i,
                    "number": i + 1,
                    "anime_id": anime.id,
                    "created_at": "2020-10-01 00:00",
                    "modified_at": "2020-10-01 00:00",
                }
            )
            for i in range(10)
        ],
    )


@pytest.fixture()
def anime_sources(anime):
    return [
        AnimeSource(
            id=55145 + i,
            source=f"/anime/narutoold/naruto-{i+1:03d}.mp4",
            number=i + 1,
            anime_id=anime.id,
            created_at=datetime.datetime(2020, 1, 1) + datetime.timedelta(days=i),
            updated_at=datetime.datetime(
                2020,
                1,
                1,
            )
            + datetime.timedelta(days=i),
        )
        for i in range(100)
    ]
