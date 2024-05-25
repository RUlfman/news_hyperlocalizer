from dotenv import load_dotenv
from stories.models import Story
from django.db.models import Q
import random
import requests
import os


# Load environment variables from .env file
load_dotenv()


def evaluate_stories_userneeds(date=None):
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
    api_key = os.getenv('SMARTOCTO_API_KEY')

    if api_key:
        url = "https://api.contentinsights.com/api/v2/analyze"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "cpi_perspective": "user_needs"
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return {
                'needsKnow': result.get('know', 0),
                'needsUnderstand': result.get('context', 0),
                'needsFeel': result.get('emotion', 0),
                'needsDo': result.get('action', 0)
            }
        else:
            print(f"POST API call to {url} failed with status code: {response.status_code}")
            return generate_random_userneeds()
    else:
        return generate_random_userneeds()

def generate_random_userneeds():
    return {
        'needsKnow': random.randint(0, 100),
        'needsUnderstand': random.randint(0, 100),
        'needsFeel': random.randint(0, 100),
        'needsDo': random.randint(0, 100)
    }