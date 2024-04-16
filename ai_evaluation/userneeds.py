from stories.models import Story
from django.db.models import Q
import random


def evaluate_stories(date=None):
    if date is None:
        stories = Story.objects.filter(needsKnow=0, needsUnderstand=0, needsFeel=0, needsDo=0)
    else:
        stories = Story.objects.filter(Q(created=date) | Q(updated=date))
    for story in stories:
        evaluate_story_userneeds(story)


def evaluate_story_userneeds(story):
    user_needs = evaluate_userneeds(story.story)
    for field, value in user_needs.items():
        setattr(story, field, value)
    story.save()


def evaluate_userneeds(text):
    # Do something with text like pass it to the external SmartOcto API.
    # For now, we're returning a random value between 0 and 100 for each user-need
    return {
        'needsKnow': random.randint(0, 100),
        'needsUnderstand': random.randint(0, 100),
        'needsFeel': random.randint(0, 100),
        'needsDo': random.randint(0, 100)
    }
