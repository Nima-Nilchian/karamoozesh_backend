from django.contrib import admin
from .models import *


@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass
