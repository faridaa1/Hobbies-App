from django.contrib import admin
from .models import UserHobby, CustomUser, Hobby, Friendship


class UserHobbyInline(admin.TabularInline):
    """Display Hobby table inline another model"""
    model: UserHobby = UserHobby
    extra: int = 0 # Number of (add hobby) forms to show

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    """Display hobby name and desription and make them searchable"""
    list_display: tuple[str] = ('name', 'description')
    search_fields: tuple[str] = ('name', 'description')


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    """Display all friendships, allowing records to be searched and filtered"""
    list_display: tuple[str] = ('user1', 'user2', 'status')
    list_filter: tuple[str] = ('user1', 'user2', 'status')
    search_fields: tuple[str] = ('user1', 'user2', 'status')


@admin.register(CustomUser)
class CustomUserView(admin.ModelAdmin):
    """Display user fields and allow some to be filtered or searched"""
    list_display: tuple[str] = ('username', 'name', 'email', 'date_of_birth', 'is_staff', 'is_active')
    list_filter: tuple[str] = ('date_of_birth', 'is_staff', 'is_active')
    search_fields: tuple[str] = ('username', 'name', 'email')
    inlines: tuple[type] = (UserHobbyInline,)