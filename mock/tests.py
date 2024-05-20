from django.test import TestCase
import pytest
import unittest
from unittest.mock import patch, MagicMock
from mock.mockdata import import_sources_from_csv, clear_data, create_labels, populate_stories
from sources.models import Source
from stories.models import Story, LabelType
import os


class TestImportSourcesFromCSV(unittest.TestCase):
    @patch('builtins.open')
    @patch('csv.DictReader')
    @pytest.mark.django_db
    def test_import_sources_from_csv(self, mock_dict_reader, mock_open):
        csv_file_path = 'test.csv'
        mock_file = MagicMock()
        mock_open.return_value = mock_file
        mock_reader = MagicMock()
        mock_dict_reader.return_value = mock_reader

        # Mock data
        mock_data = [
            {'country': 'Nederland', 'province': 'Noord-Brabant', 'region': 'West-Brabant', 'municipality': 'West-Brabant', 'name': 'Source 1', 'website': 'www.example.com', 'medium': 'Nieuwssite', 'originalContent': 'YES', 'releaseFrequency': 'DAILY', 'commercialPublisher': 'NO', 'publisher': 'Publisher 1', 'individualOrOrganisation': 'ORGANIZATION', 'contentType': 'JOURNALISM', 'contentArea': 'West-Brabant', 'contentQuality': 'HIGH'},
            {'country': 'Nederland', 'province': 'Noord-Brabant', 'region': 'West-Brabant', 'municipality': 'West-Brabant', 'name': 'Source 2', 'website': 'www.example.org', 'medium': 'Nieuwssite', 'originalContent': 'YES', 'releaseFrequency': 'DAILY', 'commercialPublisher': 'NO', 'publisher': 'Publisher 2', 'individualOrOrganisation': 'ORGANIZATION', 'contentType': 'JOURNALISM', 'contentArea': 'West-Brabant', 'contentQuality': 'MEDIUM'}
        ]
        mock_reader.__iter__.return_value = iter(mock_data)

        # Test function
        import_sources_from_csv(csv_file_path)

        # Assertions
        self.assertEqual(Source.objects.count(), 2)
        self.assertTrue(Source.objects.filter(name='Source 1').exists())
        self.assertTrue(Source.objects.filter(name='Source 2').exists())

        # Clean up
        try:
            os.remove(csv_file_path)
        except FileNotFoundError:
            pass

class TestClearData(unittest.TestCase):
    @pytest.mark.django_db
    def test_clear_data(self):
        # Create some dummy data
        Source.objects.create(name='Test Source', website='www.example.com', country='US')
        Story.objects.create(title='Test Story', summary='Test summary', story='Test story')

        # Test function
        clear_data()

        # Assertions
        self.assertEqual(Source.objects.count(), 0)
        self.assertEqual(Story.objects.count(), 0)


class TestPopulateStories(unittest.TestCase):
    @pytest.mark.django_db
    def test_populate_stories(self):
        # Create some dummy data
        Source.objects.create(name='Test Source', website='www.example.com', country='US')

        # Test function
        populate_stories()

        # Assertions
        self.assertTrue(Story.objects.exists())

class TestCreateLabels(unittest.TestCase):
    @patch('stories.models.Label.objects.get_or_create')
    @pytest.mark.django_db
    def test_create_labels(self, mock_get_or_create):
        # Call the function
        create_labels()

        # Check if the get_or_create method was called at least once for each label type
        call_args_list = [call[1] for call in mock_get_or_create.call_args_list]  # Extract the kwargs of each call
        called_label_types = [args['type'] for args in call_args_list]  # Extract the 'type' arg of each call

        for label_type in LabelType:
            self.assertIn(label_type, called_label_types)

if __name__ == '__main__':
    unittest.main()