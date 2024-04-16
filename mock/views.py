from django.shortcuts import render
from django.http import HttpResponse
from mock.mockdata import populate_mock_data


def populate_mock_data_view(request):
    populate_mock_data()
    return HttpResponse("Mock data populated successfully!")
