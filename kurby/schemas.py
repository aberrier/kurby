import datetime
from typing import Optional, List

import typer
from pydantic import BaseModel


class AnimeSlug(BaseModel):
    id: int
    slug: str
    anime_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Anime(BaseModel):
    id: int
    title: str
    alt_title: Optional[str]
    season: int
    ongoing: int
    hb_id: Optional[int]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    hidden: bool
    mal_id: Optional[int]
    slug: AnimeSlug

    def full_title(self, stylized=False) -> str:
        alt_title = f"{f' ({self.alt_title})' if self.alt_title else ''}"
        if stylized:
            return typer.style(f"{self.title}", bold=True) + alt_title
        return f"{self.title}{alt_title}"


class AnimeEpisode(BaseModel):
    id: int
    number: int
    anime_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AnimeDetails(Anime):
    description: Optional[str]
    episodes: List[AnimeEpisode]


class AnimeSource(BaseModel):
    id: int
    source: str
    number: int
    anime_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
