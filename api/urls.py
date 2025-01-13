"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import main_spa, signup, login, logout, hobbies_api_view, user_api_view, all_users_api_view, users_api_view, user_hobbies_api_view, friendship_api_view, profile_api_view, check_password_api_view, friendship_update_api_view, potential_matches_api_view

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('signup/', signup, name='signup'),  # Signup user
    path('login/', login, name='login'),  # Login user
    path('logout/', logout, name='logout'),  # Logout user
    path('api/hobbies/', hobbies_api_view, name='hobbies'),
    path('api/friendship/<int:id>/', friendship_update_api_view, name='edit friendship'),
    path('api/user/', user_api_view, name='user'),
    path("api/potential-matches/", potential_matches_api_view, name="potential_matches"),
    path('api/users/', all_users_api_view, name='all_users_api'),
    path('api/all-users/', users_api_view, name='users'),
    path('api/user/<int:id>/<str:field>/', profile_api_view, name='profile'),
    path('api/user/<int:id>/password/<str:password>/', check_password_api_view, name='check password'),
    path('api/user/hobbies/<str:id>/', user_hobbies_api_view, name='user hobbies'),
    path('api/user/<int:from_id>/friendship/<str:to_username>/', friendship_api_view, name='friendship'),
    re_path(r'.*', main_spa),
]