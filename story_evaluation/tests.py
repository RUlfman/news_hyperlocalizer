from django.test import TestCase
import unittest
from unittest.mock import patch, MagicMock

from .models import Story, Label, StoryLabel, LabelType
from story_evaluation.story_userneeds import evaluate_userneeds
from story_evaluation.story_labels import collect_labels_for_story, classify_story


# Unit tests for story_evaluation/story_userneeds.py
class EvaluateUserNeedsTestCase(TestCase):
    @patch('story_evaluation.story_userneeds.requests.post')
    @patch('os.getenv')
    def test_evaluate_userneeds_with_api_key(self, mock_getenv, mock_post):
        # Arrange
        expected_response = {
            'know': 80,
            'context': 70,
            'emotion': 60,
            'action': 50
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = expected_response
        mock_getenv.return_value = 'test_api_key'

        # Act
        user_needs = evaluate_userneeds("Sample text")

        # Assert
        self.assertEqual(user_needs['needsKnow'], expected_response['know'])
        self.assertEqual(user_needs['needsUnderstand'], expected_response['context'])
        self.assertEqual(user_needs['needsFeel'], expected_response['emotion'])
        self.assertEqual(user_needs['needsDo'], expected_response['action'])

    @patch('story_evaluation.story_userneeds.requests.post')
    @patch('os.getenv')
    def test_evaluate_userneeds_without_api_key(self, mock_getenv, mock_post):
        # Arrange
        mock_post.return_value.status_code = 401  # Unauthorized status code
        mock_getenv.return_value = ''

        # Act
        user_needs = evaluate_userneeds("Sample text")

        # Assert
        for key, value in user_needs.items():
            self.assertTrue(0 <= value <= 100, f"Value of {key} is not between 0 and 100: {value}")


# Unit tests for story_evaluation/story_labels.py
class CollectLabelsForStoryTestCase(unittest.TestCase):
    @patch('story_evaluation.story_labels.process_content_with_openai')
    def test_collect_labels_for_story_with_items_key(self, mock_process_content_with_openai):
        # Arrange
        mock_process_content_with_openai.return_value = '{"items": [{"name": "Test Label", "type": "Test Type", "confidence": 0.9}]}'
        mock_story = MagicMock()

        # Act
        labels = collect_labels_for_story(mock_story)

        # Assert
        self.assertEqual(len(labels), 1)
        self.assertEqual(labels[0]['name'], 'Test Label')
        self.assertEqual(labels[0]['type'], 'Test Type')
        self.assertEqual(labels[0]['confidence'], 0.9)

    @patch('story_evaluation.story_labels.process_content_with_openai')
    def test_collect_labels_for_story_with_labels_key(self, mock_process_content_with_openai):
        # Arrange
        mock_process_content_with_openai.return_value = '{"labels": [{"name": "Test Label", "type": "Test Type", "confidence": 0.9}]}'
        mock_story = MagicMock()

        # Act
        labels = collect_labels_for_story(mock_story)

        # Assert
        self.assertEqual(len(labels), 1)
        self.assertEqual(labels[0]['name'], 'Test Label')
        self.assertEqual(labels[0]['type'], 'Test Type')
        self.assertEqual(labels[0]['confidence'], 0.9)

    @patch('story_evaluation.story_labels.process_content_with_openai')
    def test_collect_labels_for_story_with_invalid_json(self, mock_process_content_with_openai):
        # Arrange
        mock_process_content_with_openai.return_value = 'Invalid JSON'
        mock_story = MagicMock()

        # Act
        labels = collect_labels_for_story(mock_story)

        # Assert
        self.assertEqual(labels, [])

    @patch('story_evaluation.story_labels.StoryLabel')
    @patch('story_evaluation.story_labels.Label.objects.get_or_create')
    @patch('story_evaluation.story_labels.collect_labels_for_story')
    def test_classify_story_valid_case(self, mock_collect_labels_for_story, mock_get_or_create, mock_StoryLabel):
        # Arrange
        mock_story = MagicMock(Story)
        mock_story._state = MagicMock()
        mock_story._state.db = 'default'
        mock_label = MagicMock(Label)
        mock_label._state = MagicMock()
        mock_label._state.db = 'default'
        mock_get_or_create.return_value = (mock_label, True)
        mock_StoryLabel.return_value = MagicMock(StoryLabel)
        mock_collect_labels_for_story.return_value = [{"name": "Test Label", "type": LabelType.TOPIC, "confidence": 0.9}]

        # Act
        classify_story(mock_story)

        # Assert
        mock_collect_labels_for_story.assert_called_once_with(mock_story)
        mock_get_or_create.assert_called_once_with(name__iexact="Test Label", defaults={'name': "Test Label", 'type': LabelType.TOPIC})
        mock_StoryLabel.assert_called_once_with(story=mock_story, label=mock_label, confidence=0.9)
        mock_StoryLabel.return_value.save.assert_called_once()

    # Invalid test cases
    def test_classify_story_invalid_type(self):
        self._test_classify_story_invalid_case({"name": "Test Label", "type": "Invalid Type", "confidence": 0.9})

    def test_classify_story_missing_confidence(self):
        self._test_classify_story_invalid_case({"name": "Test Label", "type": LabelType.TOPIC})

    def test_classify_story_invalid_name(self):
        self._test_classify_story_invalid_case({"name": "", "type": LabelType.TOPIC, "confidence": 0.9})

    def test_classify_story_missing_name(self):
        self._test_classify_story_invalid_case({"type": LabelType.TOPIC, "confidence": 0.9})

    @patch('story_evaluation.story_labels.StoryLabel')
    @patch('story_evaluation.story_labels.Label.objects.get_or_create')
    @patch('story_evaluation.story_labels.collect_labels_for_story')
    def _test_classify_story_invalid_case(self, test_case, mock_collect_labels_for_story, mock_get_or_create, mock_StoryLabel):
        # Arrange
        mock_story = MagicMock(Story)
        mock_story._state = MagicMock()
        mock_story._state.db = 'default'
        mock_label = MagicMock(Label)
        mock_label._state = MagicMock()
        mock_label._state.db = 'default'
        mock_get_or_create.return_value = (mock_label, True)
        mock_StoryLabel.return_value = MagicMock(StoryLabel)
        mock_collect_labels_for_story.return_value = [test_case]

        # Act
        classify_story(mock_story)

        # Assert
        mock_collect_labels_for_story.assert_called_once_with(mock_story)
        mock_get_or_create.assert_not_called()
        mock_StoryLabel.assert_not_called()
        mock_StoryLabel.return_value.save.assert_not_called()


if __name__ == '__main__':
    unittest.main()
