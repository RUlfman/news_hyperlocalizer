from django.shortcuts import render
from .models import Source


def source_index(request):
    sort_by = request.GET.get('sort', 'name')
    name_filter = request.GET.get('name')
    website_filter = request.GET.get('website')

    sources = Source.objects.all()

    if name_filter:
        sources = sources.filter(name__icontains=name_filter)
    if website_filter:
        sources = sources.filter(website__icontains=website_filter)

    if sort_by:
        sources = sources.order_by(sort_by)

    context = {
        'sources': sources,
    }
    return render(request, "sources/source_index.html", context)


def source_detail(request, pk):
    source = Source.objects.get(pk=pk)
    context = {
        'source': source,
    }
    return render(request, "sources/source_detail.html", context)
