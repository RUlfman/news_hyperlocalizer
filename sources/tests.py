from django.test import TestCase
from .models import Source
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


class SourceModelTestCase(BaseTestCase):
    def test_source_model(self):
        self.assertEqual(self.source.name, 'Example Source')
        self.assertEqual(self.source.website, 'https://example.com')
        self.assertEqual(self.source.country, 'US')
        self.assertEqual(self.source.province, 'Example Province')
        self.assertEqual(self.source.region, 'Example Region')
        self.assertEqual(self.source.municipality, 'Example Municipality')
        self.assertEqual(self.source.medium, 'Example Medium')
        self.assertEqual(self.source.originalContent, 'Original')
        self.assertEqual(self.source.releaseFrequency, 'Daily')
        self.assertEqual(self.source.commercialPublisher, 'Yes')
        self.assertEqual(self.source.publisher, 'Example Publisher')
        self.assertEqual(self.source.individualOrOrganisation, 'Organization')
        self.assertEqual(self.source.contentType, 'Example Content Type')
        self.assertEqual(self.source.contentArea, 'Example Content Area')
        self.assertEqual(self.source.contentQuality, 'High')

class SourceDetailTemplateTestCase(BaseTestCase):
    def test_source_detail_template(self):
        response = self.client.get(reverse('source_detail', args=[self.source.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.source.name)
        self.assertContains(response, self.source.website)
        self.assertContains(response, self.source.country)
        self.assertContains(response, self.source.province)
        self.assertContains(response, self.source.region)
        self.assertContains(response, self.source.municipality)
        self.assertContains(response, self.source.medium)
        self.assertContains(response, self.source.get_originalContent_display())
        self.assertContains(response, self.source.get_releaseFrequency_display())
        self.assertContains(response, self.source.get_commercialPublisher_display())
        self.assertContains(response, self.source.publisher)
        self.assertContains(response, self.source.get_individualOrOrganisation_display())
        self.assertContains(response, self.source.get_contentType_display())
        self.assertContains(response, self.source.contentArea)
        self.assertContains(response, self.source.get_contentQuality_display())


class SourceIndexTemplateTestCase(BaseTestCase):
    def test_source_index_template(self):
        response = self.client.get(reverse('source_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Locale Bronnen')
        self.assertContains(response, 'Naam')
        self.assertContains(response, 'Website')
        self.assertContains(response, self.source.name)
        self.assertContains(response, self.source.website)
