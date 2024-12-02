from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import CustomUser, Hobby

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


def signup(request: HttpRequest) -> HttpResponse:
    """View for user signup (using ssr)"""
    if request.method == "POST":
        # Create SignupForm instance and populate w/ form data
        form = SignupForm(request.POST, request.FILES)
        print(request.FILES)
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
            return redirect('http://localhost:5173/profile/')
    else:
        form = SignupForm()

    return render(request, 'api/spa/signup.html', {"form": form})


def hobbies_api_view(request: HttpRequest) -> HttpResponse:
    """ Returning all hobbies for global store."""
    return JsonResponse({
        'hobbies' : [hobby.as_dict() for hobby in Hobby.objects.all()],
    })


def user_api_view(request: HttpRequest) -> HttpResponse:
    """Defining GET and PUT for a specific user."""
    print(request.COOKIES)
    if (request.user.id):
        return JsonResponse({
            'user' : CustomUser.objects.get(pk=request.user.id).as_dict(),
        })
    return JsonResponse({
        'user' : {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "date_of_birth": "2000-01-01",  # Format as ISO date string
        "hobbies": [],  # Empty list for hobbies
        "friends": [],  # Empty list for friends
        "profile_picture": None,  # No profile picture
        }
    })