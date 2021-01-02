from pathlib import Path
from typing import Optional, List

import typer

from kurby.helpers import filter_animes
from kurby.schemas import Anime, AnimeDetails, AnimeSource


def invalid_slug_message(slug: str, animes: Optional[List[Anime]] = None):
    suggestions = filter_animes(search=slug, animes=animes, limit=3)
    message = typer.style(slug, fg=typer.colors.RED) + " anime doesn't exist.\n"
    if suggestions:
        message += "The most similar slug(s) are :\n"
        for sug in suggestions:
            message += typer.style(
                f"{sug.slug.slug} \n", fg=typer.colors.GREEN, bold=True
            )

    message += (
        "\nUse " + typer.style("animes", bold=True) + " command to get correct slug."
    )
    return message


def anime_message(anime: Anime):
    return (
        anime.full_title(stylized=True)
        + (f"\n\tSeason: {anime.season}" if anime.season else "")
        + (typer.style(" - Ongoing", fg=typer.colors.YELLOW) if anime.season else "")
        + "\n\tSlug: "
        + typer.style(anime.slug.slug, fg=typer.colors.GREEN)
        + "\n"
    )


def anime_details_message(anime_details: AnimeDetails):
    sorted_episodes = list(sorted(anime_details.episodes, key=lambda ep: ep.number))
    message = (
        typer.style(f"{anime_details.title}", bold=True)
        + f"{f' ({anime_details.alt_title})' if anime_details.alt_title else ''}"
        + (f"\n\tSeason: {anime_details.season}" if anime_details.season else "")
        + (typer.style(" - Ongoing", blink=True) if anime_details.season else "")
        + f"\n{anime_details.description or ''}\n"
    )
    if sorted_episodes:
        message += (
            "\n Episodes going from "
            + typer.style(str(sorted_episodes[0].number), bold=True)
            + " to "
            + typer.style(str(sorted_episodes[-1].number), bold=True)
            + "\n First episode uploaded at "
            + typer.style(sorted_episodes[0].created_at.isoformat(sep=" "), bold=True)
            + "\n Last episode uploaded at "
            + typer.style(sorted_episodes[-1].created_at.isoformat(sep=" "), bold=True)
        )
    return message


def download_starting_message(sources: List[AnimeSource], directory: Path):
    return (
        f"Downloading "
        + typer.style(str(len(sources)), bold=True)
        + " files into "
        + typer.style(str(directory.absolute()), bold=True, fg=typer.colors.GREEN)
        + "..."
    )
