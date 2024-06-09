from story_evaluation.story_labels import classify_story
from story_evaluation.story_userneeds import evaluate_story_userneeds


def evaluate_story(story):
    evaluate_story_userneeds(story)
    classify_story(story)