import json
from django.db import IntegrityError

from .models import Source, Story, Label, StoryLabel, LabelType
from ai_utilities.openai_utils import process_content_with_openai, JSON_SCHEMAS


def collect_labels_for_story(story, setup_prompt, answer_format):
    try:
        # If story is an ID, retrieve the Story instance
        if isinstance(story, int):
            try:
                story = Story.objects.get(id=story)
            except Source.DoesNotExist:
                print(f"No Story object found with ID {story}")
                return []

        content = f"Title: {story.title}\nSummary: {story.summary}\nStory: {story.story}"

        # Process content with OpenAI

        openai_result = process_content_with_openai(content, setup_prompt, answer_format, JSON_SCHEMAS['story_labels'])
        if openai_result is None:
            print(f"Failed to collect labels for story '{story.title}'")
            return []

        # Parse the Labels from the OpenAI result
        try:
            openai_data = json.loads(openai_result)
            if 'items' in openai_data:
                labels = openai_data['items']
            elif 'topics' in openai_data:
                labels = openai_data['topics']
            elif 'labels' in openai_data:
                labels = openai_data['labels']
            elif 'locations' in openai_data:
                labels = openai_data['locations']
            else:
                print(f"Failed to collect labels (they were mislabeled) for story '{story.title}'")
                labels = []
        except json.JSONDecodeError:
            labels = []

    except Exception:
        return []
    else:
        return labels


def save_labels(story, labels, labeltype):
    # Validate the type field
    if labeltype not in LabelType.values:
        print(f"Invalid label type: {labeltype}")
        return

    for label_data in labels:
        # Validate the label data
        if 'name' not in label_data or 'confidence' not in label_data:
            print(f"Invalid label data: {label_data}")
            continue

        # Validate the name field
        if len(label_data['name']) > 200 or len(label_data['name']) < 1:
            print(f"Invalid label name: {label_data['name']}")
            continue

        # Get or create the Label object
        label, created = Label.objects.get_or_create(name__iexact=label_data['name'],
                                                     defaults={'name': label_data['name'], 'type': labeltype})

        # Create the StoryLabel object
        story_label = StoryLabel(story=story, label=label, confidence=label_data['confidence'])

        # Save the StoryLabel object
        try:
            story_label.save()
        except IntegrityError:
            print(f"StoryLabel already exists for story '{story.title}' and label '{label.name}'")


def classify_story(story):
    # If story is an ID, retrieve the Story instance
    if isinstance(story, int):
        try:
            story = Story.objects.get(id=story)
        except Source.DoesNotExist:
            print(f"No Story object found with ID {story}")
            return

    print(f"Collecting labels for story '{story.title}'")

    topic_setup_prompt = "You are an expert in classifying news stories by topic based on IPTC NewsCodes and " \
                         "providing tags in Dutch. Your task is to read the following story and classify the text to " \
                         "return a collection of topic labels. Each label should include a name and a confidence " \
                         "score. "
    topic_answer_format = "Please use the IPTC NewsCodes aka Media Topics taxonomy, with broad specificity, " \
                          "and provide them in Dutch. Example: 'Onderwijs' NOT 'Education', 'Klimaat' NOT 'Climate'. " \
                          "You should always capitalize the first letter of nouns in the topic. Example: 'Onderwijs' " \
                          "NOT 'onderwijs', 'Wet en Regelgeving' NOT 'wet en regelgeving'. "

    topic_labels = collect_labels_for_story(story, topic_setup_prompt, topic_answer_format)
    print(f"Collected {len(topic_labels)} potential topic labels for '{story.title}'")

    save_labels(story, topic_labels, LabelType.TOPIC)

    location_setup_prompt = "You are an expert in extracting location information from stories. Your task is to read " \
                            "the following story and identify and list all relevant locations mentioned in the story. " \
                            "Focus on general locations (cities, towns, neighborhoods) that are central to the " \
                            "story's content, and avoid mentioning locations that are only tangentially referenced. " \
                            "Each label should include a name and a confidence score. "
    location_answer_format = "Please use the Dutch names for the locations. "

    location_labels = collect_labels_for_story(story, location_setup_prompt, location_answer_format)
    print(f"Collected {len(location_labels)} potential location labels for '{story.title}'")

    save_labels(story, location_labels, LabelType.LOCATION)


def classify_stories(stories):
    for story in stories:
        classify_story(story)


def test():
    # story = Story.objects.first()
    # classify_story(story)
    stories = Story.objects.all()
    classify_stories(stories)
