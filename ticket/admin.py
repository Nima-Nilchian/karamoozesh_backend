from django.contrib import admin
from django.contrib.admin import register
from .models import *


class TicketTagInline(admin.TabularInline):
    model = Tag
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'status',
        'meeting_date',
    )
    list_filter = (
        'status', 'skill_level', 'contact_way'
    )
    list_display_links = ('title',)
    list_editable = ('status',)
    search_fields = ('title', 'status', 'meeting_date')

    @staticmethod
    def full_name(obj):
        return f'{obj.firstname} {obj.lastname}'

    inlines = (
        TicketTagInline, QuestionInline, AnswerInline
    )
