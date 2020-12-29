import datetime
from typing import Optional, List

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
