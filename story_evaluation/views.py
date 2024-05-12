from django.shortcuts import render
from django.http import HttpResponse
from story_evaluation.story_userneeds import evaluate_stories_userneeds


def evaluate_userneeds_view(request):
    evaluate_stories_userneeds()
    return HttpResponse("Evaluated userneeds succesfully!")