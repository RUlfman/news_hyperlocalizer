from django.contrib import admin
from sources.models import Source


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ['name', 'website']


admin.site.register(Source, SourceAdmin)
