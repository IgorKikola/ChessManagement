from django.core.validators import RegexValidator
"""Configuration of the admin interface for microblogs."""
from django.contrib import admin
from .models import User, Club, UserInClub, Tournament, UserInTournament, Game, Stage, Group


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
@admin.register(UserInTournament)
class UserInTournamentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for UserInTournament objects."""

    list_display = [
        'user', 'tournament','is_organiser','is_co_organiser'
    ]
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Tournament objects."""

    list_display = [
        'name', 'description', 'club','organiser','max_players','deadline','finished'
    ]

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Stage objects."""

    list_display = [
        'type'
    ]

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Game objects."""

    list_display = [
        'player1', 'player2', 'tournament', 'winner'
    ]

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Group objects."""

    list_display = [
        'stage', 'players'
    ]
