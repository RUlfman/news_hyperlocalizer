import json

from .models import Source, Story
from ai_utilities.openai_utils import process_content_with_openai, JSON_SCHEMAS
from .scraping_utils import get_scraper, extract_all_urls, extract_story_content
from django.db import models
from datetime import datetime


def extract_urls_from_source(source):
    try:
        # If source is an ID, retrieve the Source instance
        if isinstance(source, int):
            try:
                source = Source.objects.get(id=source)
            except Source.DoesNotExist:
                print(f"No Source object found with ID {source}")
                return []

        # Collect the HTML content from the source
        scraper = get_scraper(source.website)
        html_content = scraper.scrape_website(source.website)
        if html_content is None:
            return []

        urls = extract_all_urls(html_content, source.website)
        content = '\n'.join(urls)

        # Process content with OpenAI
        setup_prompt = "You are a helpful assistant designed to output JSON. " \
                       "Your task is to determine which of the provided urls are news stories," \
                       "and which are not, and return only those that may be news stories. "
        answer_format = "Please return the URLs to the news stories in a JSON format " \
                        "according to the schema provided below."
        openai_result = process_content_with_openai(content, setup_prompt, answer_format,
                                                    JSON_SCHEMAS['url_collection'])
        if openai_result is None:
            return []

        # Parse the URLs from the OpenAI result
        try:
            urls = json.loads(openai_result)['items']
        except json.JSONDecodeError:
            return []

    except Exception:
        return []
    else:
        return urls


def interpret_html_content(html_content):
    story_content = extract_story_content(html_content)

    # Convert story_content to a string if it's not already
    if not isinstance(story_content, str):
        story_content = str(story_content)

    # Process content with OpenAI
    setup_prompt = "You are a helpful assistant designed to output JSON. Your task is to extract the news story from " \
                   "the given content, which includes the extracted text content, meta properties and images of a " \
                   "HTML page. Any reference to publication, creation or release dates should be considered as the " \
                   "'created' date. "
    answer_format = "Please return the story in a JSON format, extracting the following properties from the HTML " \
                    "content: " \
                    "title, created, updated, author, story, image_url" \
                    "If you cannot find one of these properties, you can leave it as a blank string."
    openai_result = process_content_with_openai(setup_prompt, story_content, answer_format,
                                                JSON_SCHEMAS['story_collection'])

    # Check if openai_result is not None before parsing it
    if openai_result is not None:
        # Parse and return the story data
        try:
            return json.loads(openai_result)
        except json.JSONDecodeError:
            return None
    else:
        return None


def generate_summary(story_data):
    # Check if the story data contains a summary
    if 'summary' in story_data and story_data['summary']:
        # If the summary is longer than 30 words, generate a new summary
        if len(story_data['summary'].split()) > 30:
            story_data['summary'] = generate_summary_from_story(story_data['story'])
    else:
        # Generate a new summary based on the story
        story_data['summary'] = generate_summary_from_story(story_data['story'])

    # Validate the summary
    if not validate_summary(story_data['story'], story_data['summary']):
        # If the summary is not valid, generate a new one
        story_data['summary'] = generate_summary_from_story(story_data['story'])

    return story_data


def generate_summary_from_story(story):
    # Process content with OpenAI
    setup_prompt = "You are a helpful assistant designed to output JSON. " \
                   "Your task is to write a summary of the given story, in the same language as the story."
    answer_format = "Please write a summary of maximum 30 words based on the story."
    openai_result = process_content_with_openai(setup_prompt, story, answer_format, JSON_SCHEMAS['story_summary'])

    # Check if openai_result is not None before parsing it
    if openai_result is not None:
        # Parse and return the summary
        try:
            return json.loads(openai_result)['summary']
        except json.JSONDecodeError:
            return None
    else:
        return None


def validate_summary(story, summary):
    # Process content with OpenAI
    setup_prompt = "You are a helpful assistant designed to output JSON. " \
                   "Your task is to validate if the given summary accurately represents the story."
    answer_format = "Does the summary accurately represent the story? Please answer with 'yes' or 'no'."
    openai_result = process_content_with_openai(setup_prompt, f"Story: {story}\nSummary: {summary}", answer_format, JSON_SCHEMAS['summary_validation'])

    # Check if openai_result is not None before parsing it
    if openai_result is not None:
        # Parse and return the validation result
        try:
            return json.loads(openai_result)['validation'] == 'yes'
        except json.JSONDecodeError:
            return False
    else:
        return False


def extract_stories_from_urls(urls, source):
    stories_scraped = 0

    for url in urls:
        # If 5 stories have been scraped, stop scraping
        if stories_scraped >= 5:
            print("5 stories have been scraped. For development purposes, stopping the scraping process.")
            break

        # Collect the HTML content from the URL
        scraper = get_scraper(url)
        html_content = scraper.scrape_website(url)

        # Interpret the HTML content into a 'story' object
        story_data = interpret_html_content(html_content)
        if story_data is None:
            continue

        # Generate a summary for the 'story' object
        story_data = generate_summary(story_data)

        # Validate the story data
        validated_story_data = sanitize_story_data(story_data)
        if validated_story_data is None:
            continue

        validated_story_data['source'] = source
        validated_story_data['url'] = url

        # Update or create the story
        Story.objects.update_or_create(url=url, defaults=validated_story_data)

        stories_scraped += 1


def sanitize_story_data(story_data):
    # Get the Story model fields
    story_fields = {f.name: f for f in Story._meta.get_fields()}

    for field_name, value in story_data.items():
        # Skip if the field is not in the Story model
        if field_name not in story_fields:
            continue

        field = story_fields[field_name]

        # Check if the field can be empty
        can_be_empty = field.null or field.blank

        # If the value is empty and the field cannot be empty, clear story data, so it's not saved
        if not value and not can_be_empty:
            print(f"The field '{field_name}' cannot be empty. Skipping this story.")
            return None

        # If the field is a DateTimeField and the value is not a valid datetime, set it to None
        if isinstance(field, models.DateTimeField):
            try:
                # Try to parse the value as a date in the ISO 8601 format
                datetime.fromisoformat(value)
            except Exception:
                print(f"The field '{field_name}' must be a valid datetime. Setting it to None.")
                story_data[field_name] = None

    # If 'created' is None but 'updated' is not None, set 'created' to 'updated' and 'updated' to None
    if story_data.get('created') is None and story_data.get('updated') is not None:
        story_data['created'] = story_data['updated']
        story_data['updated'] = None

    return story_data


def collect_stories_from_source(source):
    print(f"Collecting stories from source '{source.name}'")
    urls = extract_urls_from_source(source)
    print(f"Extracted {len(urls)} potential story URLs from source '{source.name}'")
    extract_stories_from_urls(urls, source)


def test():
    source = Source.objects.first()
    collect_stories_from_source(source)
