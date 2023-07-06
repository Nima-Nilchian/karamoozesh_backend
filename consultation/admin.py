from django.contrib import admin
from .models import *


class SkillsInline(admin.TabularInline):
    model = ConsultantSkills
    extra = 1


class SkillsFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Skills'
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'skills'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        skills = Skill.objects.all()
        return [(skill.id, skill.name) for skill in skills]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(consultant_skills__skill_id=self.value())


@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone_number', 'skills')
    list_display_links = ('user_id',)
    search_fields = ('user_id', 'phone_num')
    list_filter = (SkillsFilter,)

    @staticmethod
    def skills(obj):
        return ', '.join([s.skill_id.name for s in obj.consultant_skills.all()])

    inlines = (
        SkillsInline,
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)


