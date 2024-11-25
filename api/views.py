from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import CustomUser
from django.contrib.auth import login

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


def signup(request: HttpRequest) -> HttpResponse:
    """View for user signup (using ssr)"""
    if request.method == "POST":
        # Create SignupForm instance and populate w/ form data
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user from valid form
            data = form.cleaned_data
            user = CustomUser.objects.create_user(
                username=data['email'],
                password=data['password'],
                email=data['email'],
                name=data['name'],
                date_of_birth=data['date_of_birth'],
                profile_picture=data['profile_picture']
            )
            # TODO - auth (and context?) stuff for response
            # TODO - use reverse for urls once ^
            login(request, user)
            return redirect('http://localhost:5173/profile')
    else:
        form = SignupForm()

    return render(request, 'api/spa/signup.html', {"form": form})


def get_user(request: HttpRequest) -> JsonResponse:
    """Retrieves the User ID of the currently logged in user"""
    user : CustomUser = CustomUser.objects.get(pk=request.session.get('_auth_user_id'))
    return JsonResponse({
        'id': user.id,
        "name": user.name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "profile_picture": user.profile_picture.url if user.profile_picture else None,
    })