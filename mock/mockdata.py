from faker import Faker
from django.utils import timezone
from stories.models import Story
from sources.models import *
import os
import random
import csv


def import_sources_from_csv(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:

            original_content = getattr(OriginalContent, row['originalContent'], OriginalContent.MIX)
            release_frequency = getattr(ReleaseFrequency, row['releaseFrequency'], ReleaseFrequency.UNSURE)
            commercial_publisher = getattr(CommercialPublisher, row['commercialPublisher'], CommercialPublisher.YES)
            individual_or_organisation = getattr(IndividualOrOrganisation, row['individualOrOrganisation'], IndividualOrOrganisation.UNSURE)
            content_type = getattr(ContentType, row['contentType'], ContentType.MIX)
            content_quality = getattr(ContentQuality, row['contentQuality'], ContentQuality.LOW)

            source_data = {
                'name': row['name'],
                'website': row['website'],
                'country': row['country'],
                'province': row['province'],
                'region': row['region'],
                'municipality': row['municipality'],
                'medium': row['medium'],
                'originalContent': original_content,
                'releaseFrequency': release_frequency,
                'commercialPublisher': commercial_publisher,
                'publisher': row['publisher'],
                'individualOrOrganisation': individual_or_organisation,
                'contentType': content_type,
                'contentArea': row['contentArea'],
                'contentQuality': content_quality
            }

            Source.objects.create(**source_data)

def clear_data():
    # Clear existing data
    Story.objects.all().delete()
    Source.objects.all().delete()


def populate_sources():
    # Clear existing data
    Source.objects.all().delete()

    csv_file_path = 'uploads/csv/sources.csv'
    import_sources_from_csv(csv_file_path)


def populate_stories():
    # Clear existing data
    Story.objects.all().delete()

    fake = Faker()
    image_files = os.listdir('uploads/story_images/')

    sources = Source.objects.all()

    for source in sources:

        # Create 10 stories for each source
        for _ in range(10):
            title = fake.sentence()
            created = fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone())
            updated = fake.date_time_between(start_date=created, end_date='now', tzinfo=timezone.get_current_timezone())
            summary = fake.paragraph()
            story = ' '.join(fake.texts(nb_texts=20))
            url = fake.url()
            if image_files:
                random_image = random.choice(image_files)
                image = f'story_images/{random_image}'
            else:
                image = None
            author = fake.name()

            Story.objects.create(
                title=title,
                created=created,
                updated=updated,
                summary=summary,
                story=story,
                url=url,
                image=image,
                author=author,
                source=source
            )

