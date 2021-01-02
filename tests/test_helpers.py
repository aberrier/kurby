from unittest.mock import patch

from kurby.helpers import filter_animes, select_anime_slug


class TestHelpers:
    def test_filter_animes(self, animes, naruto_animes):
        filtered_animes = filter_animes("naruto", animes)
        assert filtered_animes == naruto_animes

    def test_download_source(self):
        pass

    @patch("kurby.helpers.prompt")
    @patch("kurby.cli.get_animes")
    def test_select_anime_slug(self, mock_animes, mock_prompt, animes, anime):
        mock_animes.return_value = animes
        mock_prompt.return_value = {"filter": "naruto", "anime": anime}
        assert select_anime_slug(None) == "naruto"
