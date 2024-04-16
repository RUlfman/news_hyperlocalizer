from django.db import models
from sources.models import Source


class Story(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    author = models.CharField(max_length=200, blank=True)
    story = models.TextField(blank=True)
    summary = models.TextField()
    url = models.URLField()
    image = models.FileField(upload_to="story_images/", blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)

    needsKnow = models.IntegerField(default=0)
    needsUnderstand = models.IntegerField(default=0)
    needsFeel = models.IntegerField(default=0)
    needsDo = models.IntegerField(default=0)

    @property
    def needs_sum(self):
        return self.needsKnow + self.needsUnderstand + self.needsFeel + self.needsDo

    @property
    def needs_primary(self):
        user_needs = {
            'know': self.needsKnow,
            'understand': self.needsUnderstand,
            'feel': self.needsFeel,
            'do': self.needsDo
        }

        max_score_field = max(user_needs, key=user_needs.get)
        return max_score_field.capitalize()

    def __str__(self):
        return self.title
