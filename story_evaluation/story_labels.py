import json
from django.db import IntegrityError

from .models import Source, Story, Label, StoryLabel, LabelType
from ai_utilities.openai_utils import process_content_with_openai, JSON_SCHEMAS

def collect_labels_for_story(story):
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
        setup_prompt = "You are a helpful assistant designed to to output JSON. " \
                       "Your task is to read the following story and classify the text to return a collection of " \
                       "labels. Each label should include a name, a type, and a confidence score. " \
                       "The type should be one of the following: LOCATION, TOPIC, CATEGORY, AUDIENCE. " \
                       "Please ensure that you return at least one label of each type, but only include labels with a " \
                       "confidence score exceeding 0.5.  "
        answer_format = "Types: CATEGORY are broad classifications. " \
                        "TOPIC are more specific themes within categories. " \
                        "LOCATION are specific places, not broad geographical tags. " \
                        "AUDIENCE are the intended target group, e.g. readers of the story. " \
                        "Please use the IPTC Media Topics taxonomy, with broad specificity and Dutch language. "
        openai_result = process_content_with_openai(content, setup_prompt, answer_format,
                                                    JSON_SCHEMAS['story_labels'])
        if openai_result is None:
            print(f"Failed to collect labels for story '{story.title}'")
            return []

        # Parse the Labels from the OpenAI result
        try:
            try:
                labels = json.loads(openai_result)['items']
            except KeyError:
                labels = json.loads(openai_result)['labels']
        except json.JSONDecodeError:
            return []

    except Exception:
        return []
    else:
        return labels


def classify_story(story):
    # If story is an ID, retrieve the Story instance
    if isinstance(story, int):
        try:
            story = Story.objects.get(id=story)
        except Source.DoesNotExist:
            print(f"No Story object found with ID {story}")
            return

    print(f"Collecting labels for story '{story.title}'")
    collected_labels = collect_labels_for_story(story)
    print(f"Collected {len(collected_labels)} potential labels for '{story.title}'")

    for label_data in collected_labels:
        # Validate the label data
        if 'name' not in label_data or 'type' not in label_data or 'confidence' not in label_data:
            print(f"Invalid label data: {label_data}")
            continue

        # Validate the name field
        if len(label_data['name']) > 200 or len(label_data['name']) < 1:
            print(f"Invalid label name: {label_data['name']}")
            continue

        # Validate the type field
        if label_data['type'] not in LabelType.values:
            print(f"Invalid label type: {label_data['type']}")
            continue

        # Get or create the Label object
        label, created = Label.objects.get_or_create(name__iexact=label_data['name'],
                                                     defaults={'name': label_data['name'], 'type': label_data['type']})

        # Create the StoryLabel object
        story_label = StoryLabel(story=story, label=label, confidence=label_data['confidence'])

        # Save the StoryLabel object
        try:
            story_label.save()
        except IntegrityError:
            print(f"StoryLabel already exists for story '{story.title}' and label '{label.name}'")


def classify_stories(stories):
    for story in stories:
        classify_story(story)


def test():
    #story = Story.objects.first()
    #classify_story(story)
    stories = Story.objects.all()
    classify_stories(stories)

