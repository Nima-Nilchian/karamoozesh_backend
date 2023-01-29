from django.contrib import admin
from django.contrib.admin import register
from .models import Subject, Link


class LinkInline(admin.StackedInline):
    model = Link
    extra = 1


@register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (LinkInline,)

