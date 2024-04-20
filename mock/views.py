from django.shortcuts import render
from django.http import HttpResponse
from mock.mockdata import populate_stories, populate_sources, clear_data


def clear_data_view(request):
    clear_data()
    return HttpResponse("Existing data cleared!")


def populate_sources_view(request):
    populate_sources()
    return HttpResponse("Sources populated successfully with CSV import!")


def populate_stories_view(request):
    populate_stories()
    return HttpResponse("Stories populated successfully with mock data!")
