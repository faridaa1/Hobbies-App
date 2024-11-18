from django.contrib import admin
from .models import UserHobby, CustomUser, Hobby, Friendship


class UserHobbyInline(admin.TabularInline):
    """Display Hobby table inline another model"""
    model = UserHobby


class FriendshipInline(admin.TabularInline):
    """Display Friendship table inline another model"""
    model = Friendship
    fk_name = 'user1'


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    """Display hobby name and desription and make them searchable"""
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(CustomUser)
class CustomUserView(admin.ModelAdmin):
    """Display user fields and allow some to be filtered or searched"""
    list_display = ('username', 'name', 'email', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('date_of_birth', 'is_staff', 'is_active')
    search_fields = ('username', 'name', 'email')
    inlines = (UserHobbyInline, FriendshipInline)