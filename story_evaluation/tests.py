from django.test import TestCase
import unittest
from unittest.mock import patch
from story_evaluation.story_userneeds import evaluate_userneeds


class EvaluateUserNeedsTestCase(TestCase):
    @patch('story_evaluation.story_userneeds.requests.post')
    @patch('os.getenv')
    def test_evaluate_userneeds_with_api_key(self, mock_getenv, mock_post):
        # Mocking response from the API
        expected_response = {
            'know': 80,
            'context': 70,
            'emotion': 60,
            'action': 50
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = expected_response

        # Mocking the environment variable
        mock_getenv.return_value = 'test_api_key'

        # Calling the function
        user_needs = evaluate_userneeds("Sample text")

        # Assertions
        self.assertEqual(user_needs['needsKnow'], expected_response['know'])
        self.assertEqual(user_needs['needsUnderstand'], expected_response['context'])
        self.assertEqual(user_needs['needsFeel'], expected_response['emotion'])
        self.assertEqual(user_needs['needsDo'], expected_response['action'])

    @patch('story_evaluation.story_userneeds.requests.post')
    @patch('os.getenv')
    def test_evaluate_userneeds_without_api_key(self, mock_getenv, mock_post):
        # Mocking response from the API
        mock_post.return_value.status_code = 401  # Unauthorized status code

        # Mocking the environment variable
        mock_getenv.return_value = ''

        # Calling the function
        user_needs = evaluate_userneeds("Sample text")

        # Assertions
        for key, value in user_needs.items():
            self.assertTrue(0 <= value <= 100, f"Value of {key} is not between 0 and 100: {value}")


if __name__ == '__main__':
    unittest.main()