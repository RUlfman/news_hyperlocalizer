from django.test import TestCase
from django.utils import timezone
from .models import Story
from sources.models import Source
from django.urls import reverse


# BaseTestCase: Contains shared setUp method. Extend this class for other test cases that need the SetUp.
class BaseTestCase(TestCase):
    def setUp(self):
        # Create a source
        self.source = Source.objects.create(
            name='Example Source',
            website='https://example.com',
            country='US',
            province='Example Province',
            region='Example Region',
            municipality='Example Municipality',
            medium='Example Medium',
            originalContent='Original',
            releaseFrequency='Daily',
            commercialPublisher='Yes',
            publisher='Example Publisher',
            individualOrOrganisation='Organization',
            contentType='Example Content Type',
            contentArea='Example Content Area',
            contentQuality='High'
        )

        # Create a story
        self.story = Story.objects.create(
            title='Test Story',
            created=timezone.now(),
            updated=timezone.now(),
            author='Test Author',
            story='Test Story Content',
            summary='Test Summary',
            url='https://example.com/test-story',
            source=self.source,
            needsKnow=20,
            needsUnderstand=30,
            needsFeel=40,
            needsDo=50
        )


class StoryModelTestCase(BaseTestCase):
    def test_needs_sum_property(self):
        expected_needs_sum = self.story.needsKnow + self.story.needsUnderstand + self.story.needsFeel + self.story.needsDo
        self.assertEqual(self.story.needs_sum, expected_needs_sum)

    def test_needs_primary_property(self):
        expected_needs_primary = 'Do'  # Since 'Do' has the highest score
        self.assertEqual(self.story.needs_primary, expected_needs_primary)

    def test_string_representation(self):
        expected_string_representation = 'Test Story'
        self.assertEqual(str(self.story), expected_string_representation)

    def test_story_creation(self):
        # Check if the story was created successfully
        self.assertTrue(Story.objects.filter(title='Test Story').exists())

    def test_story_deletion(self):
        # Delete the story and check if it was deleted successfully
        self.story.delete()
        self.assertFalse(Story.objects.filter(title='Test Story').exists())


class StoryDetailTemplateTestCase(BaseTestCase):
    def test_story_detail_template(self):
        response = self.client.get(reverse('story_detail', kwargs={'pk': self.story.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.story.title)
        self.assertContains(response, self.story.author)
        self.assertContains(response, self.story.source.name)
        self.assertContains(response, self.story.summary)
        self.assertContains(response, self.story.url)
        self.assertContains(response, f'{self.story.needsKnow}')
        self.assertContains(response, f'{self.story.needsUnderstand}')
        self.assertContains(response, f'{self.story.needsFeel}')
        self.assertContains(response, f'{self.story.needsDo}')

    def test_story_index_template(self):
        response = self.client.get(reverse('story_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Locale verhalen')
        self.assertContains(response, 'Sort by:')
        self.assertContains(response, 'Filter by title:')
        self.assertContains(response, 'Filter by created date:')
        self.assertContains(response, 'Filter by source:')
        self.assertContains(response, 'Apply Filters')
        self.assertContains(response, self.story.title)
        self.assertContains(response, self.story.source.name)
        self.assertContains(response, f'{self.story.needs_sum}')
        self.assertContains(response, f'{self.story.needs_primary}')
