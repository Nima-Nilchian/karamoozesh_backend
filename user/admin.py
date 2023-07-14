from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, FavoriteCVs, UserSurvey
from django.contrib.auth.hashers import make_password


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
    list_display = ('id', 'email', 'is_active', 'is_consultant')
    list_display_links = ('id', 'email')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('email',)
    inlines = (ProfileInline, SurveyInline, FavoriteCVsInline)

    def save_model(self, request, obj, form, change):
        """ Hash password manually (receive raw password in admin) """
        raw_password = form.cleaned_data.get('password')
        hashed_password = make_password(raw_password)
        obj.password = hashed_password
        super().save_model(request, obj, form, change)
