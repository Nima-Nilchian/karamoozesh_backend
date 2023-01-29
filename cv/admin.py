from django.contrib import admin
from django.contrib.admin import register
from .models import CV, Language, Work, Education,\
    Skill, Certificate, Project, Link


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1


class WorkInline(admin.StackedInline):
    model = Work
    extra = 1


class EducationInline(admin.StackedInline):
    model = Education
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill


class CertificateInline(admin.StackedInline):
    model = Certificate
    extra = 1


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1


class LinkInline(admin.TabularInline):
    model = Link
    extra = 2


@register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 'full_name', 'gender', 'city',
        'suggested_salary', 'is_active'
    )
    list_filter = (
        'gender', 'duty_system', 'martial_status',
        'character', 'is_active', 'city'
    )
    list_display_links = ('user_id', 'full_name')
    list_editable = ('is_active',)
    search_fields = ('full_name', 'about_me', 'phone_number', 'address', 'user_id')

    @staticmethod
    def full_name(obj):
        return f'{obj.firstname} {obj.lastname}'

    inlines = (
        LanguageInline, WorkInline, EducationInline, SkillInline,
        CertificateInline, ProjectInline, LinkInline
    )
