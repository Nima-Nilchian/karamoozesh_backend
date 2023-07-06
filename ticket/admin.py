from django.contrib import admin
from django.contrib.admin import register
from .models import Ticket, TicketTag, QA


class TicketTagInline(admin.TabularInline):
    model = TicketTag
    extra = 1


class QAInline(admin.StackedInline):
    model = QA
    extra = 1


@register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'status', 'phone_number',
        'meeting_date', 'skill_level'
    )
    list_filter = (
        'status', 'skill_level'
    )
    list_display_links = ('title',)
    list_editable = ('status',)
    search_fields = ('title', 'status', 'phone_number', 'meeting_date')

    @staticmethod
    def full_name(obj):
        return f'{obj.firstname} {obj.lastname}'

    inlines = (
        TicketTagInline, QAInline
    )
