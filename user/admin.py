from django.contrib import admin
from django.contrib.admin import register
from .models import User, Profile, FavoriteCVs, UserSurvey


class ProfileInline(admin.TabularInline):
    model = Profile


class FavoriteCVsInline(admin.TabularInline):
    model = FavoriteCVs
    extra = 1


class SurveyInline(admin.TabularInline):
    model = UserSurvey
    extra = 1


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active')
    list_display_links = ('id', 'email')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('email',)
    inlines = (ProfileInline, SurveyInline, FavoriteCVsInline)
