from django.contrib import admin
from .models import *


class SkillsInline(admin.StackedInline):
    model = ConsultantSkills
    extra = 1


@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'phone_number', 'skills']
    inlines = [SkillsInline]

    def skills(self, obj):
        return ','.join([s.skill_id.name for s in obj.consultant_skills.all()])


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']


