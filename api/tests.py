# URLS tests
from django.test import SimpleTestCase
from django.urls import resolve


class TestUrls(SimpleTestCase):

    def test_token_url(self):
        url = reverse('api-token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, ObtainTokenPairView)

    def test_source_list_create_url(self):
        url = reverse('source-list-create')
        self.assertEqual(resolve(url).func.view_class, SourceListCreate)
        self.assertEqual(resolve(url).func.view_class.permission_classes, [IsAuthenticated])

    def test_source_retrieve_update_destroy_url(self):
        url = reverse('source-detail', args=[1])  # Assuming the pk is 1
        self.assertEqual(resolve(url).func.view_class, SourceRetrieveUpdateDestroy)
        self.assertEqual(resolve(url).func.view_class.permission_classes, [IsAuthenticated])

    def test_story_list_create_url(self):
        url = reverse('story-list-create')
        self.assertEqual(resolve(url).func.view_class, StoryListCreate)
        self.assertEqual(resolve(url).func.view_class.permission_classes, [IsAuthenticated])

    def test_story_retrieve_update_destroy_url(self):
        url = reverse('story-detail', args=[1])  # Assuming the pk is 1
        self.assertEqual(resolve(url).func.view_class, StoryRetrieveUpdateDestroy)
        self.assertEqual(resolve(url).func.view_class.permission_classes, [IsAuthenticated])



# Views tests
from django.test import TestCase
from .views import *
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_source_list_create_view(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('source-list-create')
        response = self.client.post(url, {'name': 'Test Source'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test GET with query parameters
        response = self.client.get(url, {'name': 'Test Source'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.data['results']:
            self.assertEqual(response.data['results'][0]['name'], 'Test Source')

    def test_source_retrieve_update_destroy_view(self):
        self.client.force_authenticate(user=self.user)
        source = Source.objects.create(name='Test Source')
        url = reverse('source-detail', kwargs={'pk': source.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_list_create_view(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('story-list-create')
        data = {
            'title': 'Test Story',
            'story': 'Test Story Content',
            'summary': 'Test Summary',
            'url': 'https://example.com/test-story'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test GET with query parameters
        response = self.client.get(url, {'title': 'Test Story'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.data['results']:
            self.assertEqual(response.data['results'][0]['title'], 'Test Story')

    def test_story_retrieve_update_destroy_view(self):
        self.client.force_authenticate(user=self.user)
        story = Story.objects.create(title='Test Story')
        url = reverse('story-detail', kwargs={'pk': story.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Serializers tests
from django.test import TestCase
from .serializers import *


class TestSerializers(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_obtain_auth_token_serializer(self):
        serializer = ObtainAuthTokenSerializer(data={'username': 'testuser', 'password': 'testpassword'})
        self.assertTrue(serializer.is_valid())
        self.assertIn('token', serializer.validated_data)

        # Test with invalid credentials
        serializer = ObtainAuthTokenSerializer(data={'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertFalse(serializer.is_valid())

    def test_story_serializer(self):
        data = {
            'title': 'Test Story',
            'story': 'Test Story Content',
            'summary': 'Test Summary',
            'url': 'https://example.com/test-story'
        }
        serializer = StorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_source_serializer(self):
        serializer = SourceSerializer(data={'name': 'Test Source'})
        self.assertTrue(serializer.is_valid())
