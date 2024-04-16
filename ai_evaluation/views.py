from django.shortcuts import render
from django.http import HttpResponse
from ai_evaluation.userneeds import evaluate_stories


def evaluate_userneeds_view(request):
    evaluate_stories()
    return HttpResponse("Evaluated userneeds succesfully!")