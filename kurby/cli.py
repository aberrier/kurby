#!/usr/bin/env python

import datetime
from pathlib import Path
from typing import Optional

import typer
from faker import Faker

from kurby.constants import (
    ANIME_SLUG_HELP,
    CWD_DIR,
    TWIST_SUPPORTING_MESSAGE,
    ANIMES_COMMAND_NAME,
    DETAILS_COMMAND_NAME,
    DOWNLOAD_COMMAND_NAME,
    UPDATE_COMMAND_NAME,
)
from kurby.helpers import (
    download_source,
    filter_animes,
    select_anime_slug,
)
from kurby.api import get_animes, get_anime_details, get_sources
from kurby.messages import (
    invalid_slug_message,
    anime_message,
    anime_details_message,
    download_starting_message,
)
from kurby.utils import slugify, check_for_update, get_current_version, install_package

app = typer.Typer(
    help="""
    A nice CLI to download animes from twist.moe
    
    The developer or this application do not store any animes whatsoever
    
    If you want to contribute to the list of animes please consider donating to twist.moe
"""
)
fake = Faker()

payload = {}


def start():
    app()


@app.callback()
def main(check_updates: bool = typer.Option(True, help="Check for Kurby updates")):
    typer.echo(TWIST_SUPPORTING_MESSAGE)
    if check_updates:
        current_version = get_current_version()
        version = check_for_update(current_version=current_version)
        if version:
            typer.echo(
                "You are using Kurby "
                + typer.style(current_version, bold=True, fg=typer.colors.RED)
                + " while version "
                + typer.style(version, bold=True, fg=typer.colors.GREEN)
                + " is available.\nUse "
                + typer.style(UPDATE_COMMAND_NAME, bold=True)
                + " command to update to the latest version !\n"
            )


@app.command(name=ANIMES_COMMAND_NAME)
def display_animes(
    search: Optional[str] = typer.Option(None, help="Filter results with fuzzy search")
):
    """
    Search and display information about available animes and optionally use --search to fuzzy search

    Among the information given, the slug is what is used in other commands
    """
    animes = get_animes()
    if search:
        animes = filter_animes(search, animes)

    for anime in animes:
        typer.echo(anime_message(anime))


@app.command(name=DETAILS_COMMAND_NAME)
def display_anime_details(
    slug: str = typer.Argument(None, help=ANIME_SLUG_HELP, callback=select_anime_slug),
):
    """
    Give more details on a specific anime like the number of episodes from a given anime slug
    """
    animes = get_animes()
    animes_by_slug = {anime.slug.slug: anime for anime in animes}
    try:
        anime = animes_by_slug[slug]
    except KeyError:
        raise typer.BadParameter(invalid_slug_message(slug=slug, animes=animes))
    typer.echo(anime_details_message(get_anime_details(anime)))


@app.command(name=DOWNLOAD_COMMAND_NAME)
def download(
    slug: str = typer.Argument(None, help=ANIME_SLUG_HELP, callback=select_anime_slug),
    directory: str = typer.Option(
        CWD_DIR, "--d", help="Directory where files will be uploaded"
    ),
    nfrom: int = typer.Option(
        None, "--nfrom", help="Select episodes greater or equal to the given number"
    ),
    nto: int = typer.Option(
        None, "--nto", help="Select episodes lesser or equal to the given number"
    ),
    dfrom: datetime.datetime = typer.Option(
        None, "--dfrom", help="Select episodes uploaded after the given date"
    ),
    dto: datetime.datetime = typer.Option(
        None, "--dto", help="Select episodes uploaded before the given date"
    ),
):
    """
    Download a list of episodes from a given anime slug

    The output directory can be specified
    """
    directory = Path(directory)
    animes = get_animes()
    animes_by_slug = {anime.slug.slug: anime for anime in animes}
    try:
        anime = animes_by_slug[slug]
    except KeyError:
        raise typer.BadParameter(invalid_slug_message(slug=slug, animes=animes))
    sources = get_sources(anime)
    filtered_source_ids = set(source.id for source in sources)
    if nfrom:
        if type(nfrom) is int:
            filtered_source_ids -= set(
                source.id for source in sources if source.number < nfrom
            )
    if dfrom:
        filtered_source_ids -= set(
            source.id for source in sources if source.created_at < dfrom
        )
    if nto:
        filtered_source_ids -= set(
            source.id for source in sources if source.number > nto
        )

    if dto:
        filtered_source_ids -= set(
            source.id for source in sources if source.created_at > dto
        )

    sources = list(
        sorted(
            (source for source in sources if source.id in filtered_source_ids),
            key=lambda s: s.number,
        )
    )
    if not sources:
        typer.secho("No sources to download ! ", bold=True)
        raise typer.Exit(code=1)
    typer.echo(download_starting_message(sources=sources, directory=directory))
    for source in sources:
        typer.echo(f"{anime.title} - S{anime.season:02d} - E{source.number:02d}")
        title_slug = slugify(anime.title)
        current_dir = directory / title_slug
        if not current_dir.exists():
            current_dir.mkdir(parents=True, exist_ok=True)
        ext = source.source.rsplit(".", 1)[-1]
        filepath = (
            current_dir / f"{title_slug}-S{anime.season:02d}-E{source.number:03d}.{ext}"
        )
        download_source(source, filepath)


@app.command(name=UPDATE_COMMAND_NAME)
def update():
    """
    Update Kurby to the latest version
    """
    try:
        current_version = get_current_version()
        version = check_for_update(current_version=current_version)
        if version:
            install_package(version)
        else:
            typer.echo("You are using the latest version !")
    except Exception:
        typer.secho(
            "The installation of Kurby failed. Please reinstall it manually.",
            fg=typer.colors.RED,
        )
        raise


if __name__ == "__main__":
    start()
