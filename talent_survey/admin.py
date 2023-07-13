from django.contrib import admin
from django.contrib.admin import register
from .models import TalentSurvey


@register(TalentSurvey)
class TalentSurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'result')
    search_fields = ('name',)
