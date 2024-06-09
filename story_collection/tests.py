import unittest
import json
from unittest.mock import patch, MagicMock

import requests

from story_collection import collection
from story_collection.scraping_utils import StaticWebsiteScraper


# Tests for story_collection/collection.py
class TestCollection(unittest.TestCase):
    @patch('story_collection.collection.get_scraper')
    @patch('story_collection.collection.process_content_with_openai')
    @patch('os.environ', {'OPENAI_API_KEY': 'test_openai_api_key' })
    def test_extract_urls_from_source(self, mock_process_content_with_openai, mock_get_scraper):
        # Arrange
        mock_scraper = MagicMock()
        mock_get_scraper.return_value = mock_scraper
        mock_scraper.scrape_website.return_value = "<html></html>"
        mock_process_content_with_openai.return_value = '{"items": ["http://example.com/story1", "http://example.com/story2"]}'
        source = MagicMock()

        # Act
        result = collection.extract_urls_from_source(source)

        # Assert
        self.assertEqual(result, ["http://example.com/story1", "http://example.com/story2"])
        mock_get_scraper.assert_called_once_with(source.website)
        mock_scraper.scrape_website.assert_called_once_with(source.website)
        mock_process_content_with_openai.assert_called_once()

    @patch('story_collection.collection.get_scraper')
    @patch('story_collection.collection.process_content_with_openai')
    @patch('os.environ', {'OPENAI_API_KEY': 'test_openai_api_key' })
    def test_extract_urls_from_source_with_invalid_source(self, mock_process_content_with_openai, mock_get_scraper):
        # Arrange
        mock_get_scraper.side_effect = Exception
        source = MagicMock()

        # Act
        result = collection.extract_urls_from_source(source)

        # Assert
        self.assertEqual(result, [])

    @patch('story_collection.collection.get_scraper')
    @patch('story_collection.collection.process_content_with_openai')
    @patch('story_collection.collection.extract_story_content')
    @patch('story_collection.collection.Story.objects.update_or_create')
    @patch('story_collection.collection.validate_summary')
    @patch('os.environ', {'OPENAI_API_KEY': 'test_openai_api_key' })
    def test_extract_stories_from_urls(self, mock_validate_summary, mock_update_or_create, mock_extract_story_content, mock_process_content_with_openai, mock_get_scraper):
        # Arrange
        mock_scraper = MagicMock()
        mock_get_scraper.return_value = mock_scraper
        mock_scraper.scrape_website.return_value = "<html></html>"
        mock_extract_story_content.return_value = "Test Story Content"
        mock_process_content_with_openai.return_value = '{"title": "Test Title", "created": "2022-01-01T00:00:00Z", "updated": "2022-01-01T00:00:00Z", "author": "Test Author", "story": "Test Story", "summary": "Test Summary", "image_url": "http://example.com/image.jpg"}'
        mock_validate_summary.return_value = True
        urls = ["http://example.com/story1", "http://example.com/story2"]
        source = MagicMock()

        # Act
        collection.extract_stories_from_urls(urls, source)

        # Assert
        mock_get_scraper.assert_called()
        mock_scraper.scrape_website.assert_any_call("http://example.com/story1")
        mock_scraper.scrape_website.assert_any_call("http://example.com/story2")
        mock_extract_story_content.assert_called()
        mock_process_content_with_openai.assert_called()
        mock_update_or_create.assert_called()
        mock_validate_summary.assert_called()

    def test_sanitize_story_data(self):
        # Arrange
        story_data = {
            "title": "Test Title",
            "created": "xxxx",
            "updated": "2022-01-01T00:00:00Z",
            "author": "Test Author",
            "story": "Test Story",
            "summary": "Test Summary",
            "image_url": "http://example.com/image.jpg"
        }
        expected_output = {
            "title": "Test Title",
            "created": "2022-01-01T00:00:00Z",
            "updated": None,
            "author": "Test Author",
            "story": "Test Story",
            "summary": "Test Summary",
            "image_url": "http://example.com/image.jpg"
        }

        # Act
        result = collection.sanitize_story_data(story_data)

        # Assert
        self.assertEqual(result, expected_output)


# Tests for story_collection/scraping_utils.py
class TestScrapingUtils(unittest.TestCase):
    @patch('requests.get')
    def test_static_website_scraper(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_get.return_value = mock_response
        mock_response.raise_for_status.return_value = None
        mock_response.content = "<html></html>"
        scraper = StaticWebsiteScraper()

        # Act
        result = scraper.scrape_website("http://example.com")

        # Assert
        self.assertEqual(result, "<html></html>")
        mock_get.assert_called_once_with("http://example.com")
        mock_response.raise_for_status.assert_called_once()

    @patch('requests.get')
    def test_static_website_scraper_with_invalid_url(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.exceptions.RequestException
        scraper = StaticWebsiteScraper()

        # Act
        result = scraper.scrape_website("http://invalid-url")

        # Assert
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()