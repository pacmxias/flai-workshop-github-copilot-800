from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team_name', 'role', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('role', 'created_at')
    ordering = ('-created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'activity_type', 'duration', 'distance', 'calories', 'date')
    search_fields = ('user_name', 'user_email', 'activity_type')
    list_filter = ('activity_type', 'date')
    ordering = ('-date',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user_name', 'team_name', 'total_calories', 'total_distance', 'total_activities')
    search_fields = ('user_name', 'team_name')
    list_filter = ('team_name',)
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'difficulty', 'category', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('difficulty', 'category', 'created_at')
    ordering = ('-created_at',)
