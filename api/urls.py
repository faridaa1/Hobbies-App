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
from django.urls import path

from .views import main_spa, signup, hobbies_api_view, user_api_view, hobby_api_view, user_hobbies_api_view, friendship_api_view

urlpatterns = [
    path('', main_spa),
    path('signup/', signup, name='signup'),  # Signup user
    path('api/hobby/', hobby_api_view, name='hobby'),
    path('api/hobbies/', hobbies_api_view, name='hobbies'),
    path('api/user/', user_api_view, name='user'),
    path('api/user/hobbies/<str:id>/', user_hobbies_api_view, name='user hobbies'),
    path('api/user/friendship/<int:id>/', friendship_api_view, name='friendship')
]
