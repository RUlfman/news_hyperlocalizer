from django.db import models


class OriginalContent(models.TextChoices):
    YES = 'YES', 'Yes'
    NO = 'NO', 'No'
    MIX = 'MIX', 'Mix'


class ReleaseFrequency(models.TextChoices):
    DAILY = 'DAILY', 'Daily'
    WEEKLY = 'WEEKLY', 'Weekly'
    MONTHLY = 'MONTHLY', 'Monthly'
    UNSURE = 'UNSURE', 'Changeable / Unsure'


class CommercialPublisher(models.TextChoices):
    YES = 'YES', 'Yes'
    NO = 'NO', 'No'
    UNSURE = 'UNSURE', 'Unsure'


class IndividualOrOrganisation(models.TextChoices):
    INDIVIDUAL = 'INDIVIDUAL', 'Individual'
    ORGANIZATION = 'ORGANIZATION', 'Organization'
    UNSURE = 'UNSURE', 'Unsure'


class ContentType(models.TextChoices):
    ENTERTAINMENT = 'ENTERTAINMENT', 'Entertainment'
    JOURNALISM = 'JOURNALISM', 'Journalism'
    SERVICE = 'SERVICE', 'Service provision'
    MIX = 'MIX', 'Mixed content'
    OTHER = 'OTHER', 'Other content'


class ContentQuality(models.TextChoices):
    LOW = 'LOW', 'Weak / poor'
    MEDIUM = 'MEDIUM', 'Okay, editor required'
    HIGH = 'HIGH', 'Meets journalistic requirements'


class Source(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=200, blank=True)
    province = models.CharField(max_length=200, blank=True)
    region = models.CharField(max_length=200, blank=True)
    municipality = models.CharField(max_length=200, blank=True)
    medium = models.CharField(max_length=200, blank=True)
    originalContent = models.CharField(max_length=20, choices=OriginalContent.choices, blank=True)
    releaseFrequency = models.CharField(max_length=20, choices=ReleaseFrequency.choices, blank=True)
    commercialPublisher = models.CharField(max_length=20, choices=CommercialPublisher.choices, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    individualOrOrganisation = models.CharField(max_length=20, choices=IndividualOrOrganisation.choices, blank=True)
    contentType = models.CharField(max_length=20, choices=ContentType.choices, blank=True)
    contentArea = models.CharField(max_length=200, blank=True)
    contentQuality = models.CharField(max_length=50, choices=ContentQuality.choices, blank=True)

    def __str__(self):
        return self.name
