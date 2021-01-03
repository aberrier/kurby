import datetime
import tempfile
from unittest.mock import patch

from kurby.cli import app
from kurby.constants import TWIST_SUPPORTING_MESSAGE
from kurby.messages import anime_message, anime_details_message


class TestCLI:
    @patch("kurby.cli.get_animes")
    def test_display_animes(self, mock_animes, runner, animes):
        mock_animes.return_value = animes
        result = runner.invoke(app, ["--no-check-updates", "animes"], color=True)
        assert result.exit_code == 0
        assert TWIST_SUPPORTING_MESSAGE in result.stdout
        for anime in animes:
            assert anime_message(anime) in result.stdout

    @patch("kurby.cli.get_animes")
    def test_display_animes_with_filter(
        self,
        mock_animes,
        runner,
        animes,
        naruto_animes,
        one_piece_animes,
        one_punch_animes,
        attack_on_titan_animes,
    ):
        mock_animes.return_value = animes
        result = runner.invoke(
            app, ["--no-check-updates", "animes", "--search", "naruto"], color=True
        )
        assert result.exit_code == 0
        assert TWIST_SUPPORTING_MESSAGE in result.stdout
        for anime in naruto_animes:
            assert anime_message(anime) in result.stdout
        for anime in one_piece_animes + one_punch_animes + attack_on_titan_animes:
            assert anime_message(anime) not in result.stdout

    @patch("kurby.cli.get_anime_details")
    @patch("kurby.cli.get_animes")
    def test_display_anime_details(
        self, mock_animes, mock_anime_details, runner, animes, anime_details
    ):
        mock_animes.return_value = animes
        mock_anime_details.return_value = anime_details
        result = runner.invoke(
            app, ["--no-check-updates", "details", animes[0].slug.slug], color=True
        )
        assert result.exit_code == 0
        assert TWIST_SUPPORTING_MESSAGE in result.stdout
        assert anime_details_message(anime_details) in result.stdout
        assert "Toto le rigolo" in result.stdout

    @patch("kurby.cli.get_anime_details")
    @patch("kurby.cli.get_animes")
    def test_display_anime_details_bad_slug(
        self, mock_animes, mock_anime_details, runner, animes, anime_details
    ):
        mock_animes.return_value = animes
        mock_anime_details.return_value = anime_details
        result = runner.invoke(
            app, ["--no-check-updates", "details", "i can't exist"], color=True
        )
        assert result.exit_code == 2
        assert "anime doesn't exist." in result.stdout

    @patch("kurby.cli.download_source")
    @patch("kurby.cli.get_sources")
    @patch("kurby.cli.get_animes")
    def test_download(
        self,
        mock_animes,
        mock_sources,
        mock_download,
        runner,
        anime,
        animes,
        anime_sources,
    ):
        mock_animes.return_value = animes
        mock_sources.return_value = anime_sources
        with tempfile.TemporaryDirectory() as directory:
            result = runner.invoke(
                app,
                ["--no-check-updates", "download", "naruto", "--d", directory],
                color=True,
            )
            assert result.exit_code == 0
            assert mock_animes.call_count == 1
            assert mock_sources.call_count == 1
            assert mock_sources.call_args[0][0] == anime
            assert len(mock_download.call_args_list) == 100
            assert [
                call[0][0] for call in mock_download.call_args_list
            ] == anime_sources
            filepaths = [str(call[0][1]) for call in mock_download.call_args_list]
            assert len(filepaths) == 100
            assert all(filepath.startswith(directory) for filepath in filepaths)

    @patch("kurby.cli.download_source")
    @patch("kurby.cli.get_sources")
    @patch("kurby.cli.get_animes")
    def test_download_filter_nfrom(
        self,
        mock_animes,
        mock_sources,
        mock_download,
        runner,
        anime,
        animes,
        anime_sources,
    ):
        mock_animes.return_value = animes
        mock_sources.return_value = anime_sources
        with tempfile.TemporaryDirectory() as directory:
            result = runner.invoke(
                app,
                [
                    "--no-check-updates",
                    "download",
                    "naruto",
                    "--d",
                    directory,
                    "--nfrom",
                    "10",
                ],
                color=True,
            )
            assert result.exit_code == 0
            assert mock_animes.call_count == 1
            assert mock_sources.call_count == 1
            assert mock_sources.call_args[0][0] == anime
            assert len(mock_download.call_args_list) == 91
            assert [call[0][0] for call in mock_download.call_args_list] == [
                source for source in anime_sources if source.number >= 10
            ]

    @patch("kurby.cli.download_source")
    @patch("kurby.cli.get_sources")
    @patch("kurby.cli.get_animes")
    def test_download_filter_nto(
        self,
        mock_animes,
        mock_sources,
        mock_download,
        runner,
        anime,
        animes,
        anime_sources,
    ):
        mock_animes.return_value = animes
        mock_sources.return_value = anime_sources
        with tempfile.TemporaryDirectory() as directory:
            result = runner.invoke(
                app,
                [
                    "--no-check-updates",
                    "download",
                    "naruto",
                    "--d",
                    directory,
                    "--nto",
                    "10",
                ],
                color=True,
            )
            assert result.exit_code == 0
            assert mock_animes.call_count == 1
            assert mock_sources.call_count == 1
            assert mock_sources.call_args[0][0] == anime
            assert len(mock_download.call_args_list) == 10
            assert [call[0][0] for call in mock_download.call_args_list] == [
                source for source in anime_sources if source.number <= 10
            ]

    @patch("kurby.cli.download_source")
    @patch("kurby.cli.get_sources")
    @patch("kurby.cli.get_animes")
    def test_download_filter_nfrom_nto(
        self,
        mock_animes,
        mock_sources,
        mock_download,
        runner,
        anime,
        animes,
        anime_sources,
    ):
        mock_animes.return_value = animes
        mock_sources.return_value = anime_sources
        with tempfile.TemporaryDirectory() as directory:
            result = runner.invoke(
                app,
                [
                    "--no-check-updates",
                    "download",
                    "naruto",
                    "--d",
                    directory,
                    "--nfrom",
                    "10",
                    "--nto",
                    "40",
                ],
                color=True,
            )
            assert result.exit_code == 0
            assert mock_animes.call_count == 1
            assert mock_sources.call_count == 1
            assert mock_sources.call_args[0][0] == anime
            assert len(mock_download.call_args_list) == 31
            assert [call[0][0] for call in mock_download.call_args_list] == [
                source for source in anime_sources if 10 <= source.number <= 40
            ]

    @patch("kurby.cli.download_source")
    @patch("kurby.cli.get_sources")
    @patch("kurby.cli.get_animes")
    def test_download_filter_dfrom(
        self,
        mock_animes,
        mock_sources,
        mock_download,
        runner,
        anime,
        animes,
        anime_sources,
    ):
        mock_animes.return_value = animes
        mock_sources.return_value = anime_sources
        with tempfile.TemporaryDirectory() as directory:
            result = runner.invoke(
                app,
                [
                    "--no-check-updates",
                    "download",
                    "naruto",
                    "--d",
                    directory,
                    "--dfrom",
                    "2020-01-10",
                ],
                color=True,
            )
            assert result.exit_code == 0
            assert mock_animes.call_count == 1
            assert mock_sources.call_count == 1
            assert mock_sources.call_args[0][0] == anime
            assert len(mock_download.call_args_list) == 91
            assert [call[0][0] for call in mock_download.call_args_list] == [
                source
                for source in anime_sources
                if source.created_at >= datetime.datetime(2020, 1, 10)
            ]

    @patch("kurby.cli.download_source")
    @patch("kurby.cli.get_sources")
    @patch("kurby.cli.get_animes")
    def test_download_filter_dto(
        self,
        mock_animes,
        mock_sources,
        mock_download,
        runner,
        anime,
        animes,
        anime_sources,
    ):
        mock_animes.return_value = animes
        mock_sources.return_value = anime_sources
        with tempfile.TemporaryDirectory() as directory:
            result = runner.invoke(
                app,
                [
                    "--no-check-updates",
                    "download",
                    "naruto",
                    "--d",
                    directory,
                    "--dto",
                    "2020-01-10",
                ],
                color=True,
            )
            assert result.exit_code == 0
            assert mock_animes.call_count == 1
            assert mock_sources.call_count == 1
            assert mock_sources.call_args[0][0] == anime
            assert len(mock_download.call_args_list) == 10
            assert [call[0][0] for call in mock_download.call_args_list] == [
                source
                for source in anime_sources
                if source.created_at <= datetime.datetime(2020, 1, 10)
            ]
