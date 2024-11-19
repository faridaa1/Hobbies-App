from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import CustomUser


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


def signup(request: HttpRequest) -> HttpResponse:
    """View for user signup (using ssr)"""
    if request.method == "POST":
        # Create SignupForm instance and populate w/ form data
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create user from valid form
            data = form.cleaned_data
            CustomUser.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                name=data['name'],
                date_of_birth=data['date_of_birth']
            )
            # TODO - auth (and context?) stuff for response
            # TODO - use reverse for urls once ^
            return redirect('/')
    else:
        form = SignupForm()

    return render(request, 'api/spa/signup.html', {"form": form})
