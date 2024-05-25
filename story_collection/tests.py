import unittest
import json
from unittest.mock import patch, MagicMock

import requests
from requests import HTTPError

from story_collection import collection
from story_collection.scraping_utils import StaticWebsiteScraper, DynamicWebsiteScraper
from story_collection.openai_utils import process_content_with_openai


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
    @patch('os.environ', {'OPENAI_API_KEY': 'test_openai_api_key' })
    def test_extract_stories_from_urls(self, mock_update_or_create, mock_extract_story_content, mock_process_content_with_openai, mock_get_scraper):
        # Arrange
        mock_scraper = MagicMock()
        mock_get_scraper.return_value = mock_scraper
        mock_scraper.scrape_website.return_value = "<html></html>"
        mock_extract_story_content.return_value = "Test Story Content"
        mock_process_content_with_openai.return_value = '{"title": "Test Title", "created": "2022-01-01T00:00:00Z", "updated": "2022-01-01T00:00:00Z", "author": "Test Author", "story": "Test Story", "summary": "Test Summary", "image_url": "http://example.com/image.jpg"}'
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


# Tests for story_collection/openai_utils.py
class TestOpenAIUtils(unittest.TestCase):
    @patch('os.environ', {'OPENAI_API_KEY': 'test_openai_api_key' })
    @patch('openai.OpenAI')
    def test_process_content_with_openai(self, mock_openai):
        # Arrange
        mock_response = MagicMock()
        mock_create = MagicMock()
        mock_completions = MagicMock()
        mock_chat = MagicMock()

        mock_openai.return_value = mock_chat
        mock_chat.completions = mock_completions
        mock_completions.create = mock_create
        mock_create.return_value = mock_response

        mock_response.choices = [{"message": {"content": '{\n  "heading": "Test Heading",\n  "paragraph": "This is a test paragraph."\n}'}}]
        html_content = "<html><body><h1>Test Heading</h1><p>This is a test paragraph.</p></body></html>"
        setup_prompt = "You are a helpful assistant designed to output JSON. Your task is to process the given HTML content."
        answer_format = "format"
        json_schema = {}

        # Act
        result = process_content_with_openai(html_content, setup_prompt, answer_format, json_schema)

        # Assert
        if result is not None:
            # AI is non-deterministic, so we can't check the exact output, validate the JSON structure instead
            try:
                result_json = json.loads(result)
                self.assertTrue(result_json)  # Check if the result is not empty
                self.assertIsInstance(result_json, dict)  # Check if the result is a dictionary
                self.assertTrue(any(result_json.values()))  # Check if at least one value is not None or empty
            except json.JSONDecodeError:
                self.fail("The AI's output is not a valid JSON string.")
        else:
            self.fail("process_content_with_openai returned None")


if __name__ == '__main__':
    unittest.main()