from django.core.validators import RegexValidator
"""Configuration of the admin interface for microblogs."""
from django.contrib import admin
from .models import User, Club, UserInClub


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'first_name', 'last_name', 'email', 'experience','personal_statement', 'is_active','password'
    ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs."""

    list_display = [
        'name', 'location', 'description'
    ]

@admin.register(UserInClub)
class UserInClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for UserInClub objects."""

    list_display = [
        'user', 'user_level', 'club'
    ]
