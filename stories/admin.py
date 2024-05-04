from django.contrib import admin
from stories.models import Story, Label


class StoryLabelInline(admin.TabularInline):
    model = Story.labels.through
    extra = 1

class StoryAdmin(admin.ModelAdmin):
    inlines = (StoryLabelInline,)

class LabelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Story, StoryAdmin)
admin.site.register(Label, LabelAdmin)