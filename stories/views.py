from django.shortcuts import render
from django.db.models import Sum
from stories.models import Story, Source


def story_index(request):
    sort_criteria = request.GET.get('sort', '-updated')
    filter_title = request.GET.get('name', '')
    filter_created = request.GET.get('created', '')
    filter_source = request.GET.get('source', '')

    # Apply sorting criteria
    if sort_criteria == '-created':
        stories = Story.objects.order_by('-created')
    elif sort_criteria == 'created':
        stories = Story.objects.order_by('created')
    elif sort_criteria == '-updated':
        stories = Story.objects.order_by('-updated')
    elif sort_criteria == 'updated':
        stories = Story.objects.order_by('updated')
    elif sort_criteria == 'title':
        stories = Story.objects.order_by('title')
    elif sort_criteria == 'source':
        stories = Story.objects.order_by('source__name')
    elif sort_criteria == '-needs_sum':
        stories = Story.objects.annotate(
            needsSum=Sum('needsKnow') + Sum('needsUnderstand') + Sum('needsFeel') + Sum('needsDo')
        ).order_by('-needsSum')
    else:
        stories = Story.objects.all()

    # Apply filters
    if filter_title:
        stories = stories.filter(title__icontains=filter_title)
    if filter_created:
        stories = stories.filter(created__date=filter_created)
    if filter_source:
        stories = stories.filter(source_id=filter_source)

    sources = Source.objects.order_by('name')

    context = {
        'stories': stories,
        'sources': sources,
    }
    return render(request, "stories/story_index.html", context)


def story_detail(request, pk):
    story = Story.objects.get(pk=pk)
    context = {
        'story': story,
    }
    return render(request, "stories/story_detail.html", context)
