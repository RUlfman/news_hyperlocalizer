from django.db import models
from sources.models import Source


class LabelType(models.TextChoices):
    LOCATION = 'LOCATION', 'Locatie'
    TOPIC = 'TOPIC', 'Onderwerp'
    CATEGORY = 'CATEGORY', 'Categorie'
    AUDIENCE = 'AUDIENCE', 'Doelgroep'

COLORS = ['#007bff', '#28a745', '#17a2b8', '#ffc107']  # Blue, Green, Cyan, Yellow

LABEL_COLORS = {label_type: color for label_type, color in zip(LabelType, COLORS)}


class Label(models.Model):
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=20, choices=LabelType.choices)

    def label_color(self):
        return LABEL_COLORS[self.type]

    def __str__(self):
        return f'{self.name}: {self.type}'


class Story(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    author = models.CharField(max_length=200, blank=True)
    story = models.TextField(blank=True)
    summary = models.TextField()
    url = models.URLField()
    image = models.FileField(upload_to="story_images/", blank=True)
    image_url = models.URLField(blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)

    needsKnow = models.IntegerField(default=0)
    needsUnderstand = models.IntegerField(default=0)
    needsFeel = models.IntegerField(default=0)
    needsDo = models.IntegerField(default=0)
    needsSum = models.IntegerField(default=0)

    needsPrimary = models.CharField(max_length=20, blank=True)

    labels = models.ManyToManyField(Label, through='StoryLabel', blank=True)

    def save(self, *args, **kwargs):

        user_needs = {
            'know': self.needsKnow,
            'understand': self.needsUnderstand,
            'feel': self.needsFeel,
            'do': self.needsDo
        }
        max_score_field = max(user_needs, key=user_needs.get)
        self.needsPrimary = max_score_field.capitalize()

        self.needsSum = self.needsKnow + self.needsUnderstand + self.needsFeel + self.needsDo

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class StoryLabel(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('story', 'label')

    def __str__(self):
        return f'{self.story.title} - {self.label.name}'