from django.contrib import admin
from .models import UserHobby, CustomUser, Hobby

# Register your models here.
class UserHobbyInline(admin.TabularInline):
    model = UserHobby

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('date_of_birth', 'is_staff', 'is_active')
    search_fields = ('username', 'name', 'email')
    inlines = (UserHobbyInline,)