import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from .models import CustomUser, Hobby, UserHobby

URL = 'http://localhost:5173/'


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
            CustomUser.objects.create_user(
                username=data['email'],
                password=data['password'],
                email=data['email'],
                name=data['name'],
                date_of_birth=data['date_of_birth'],
                profile_picture=data['profile_picture']
            )
            user = authenticate(  # verifies details
                request, username=data['email'], password=data['password'])
            if user is not None:
                login(request, user)  # logs in user and saves id in session
            return redirect('http://localhost:5173/profile/')
    else:
        form = SignupForm()

    return render(request, 'api/spa/signup.html', {"form": form})


def hobbies_api_view(request: HttpRequest) -> HttpResponse:
    """ Returning all hobbies for global store."""
    return JsonResponse({
        'hobbies': [hobby.as_dict() for hobby in Hobby.objects.all()],
    })


def user_api_view(request: HttpRequest) -> HttpResponse:
    """Defining GET and PUT for a specific user."""
    print(request.COOKIES)
    print(request.user)
    if (request.user.is_authenticated):
        return JsonResponse({
            'user': CustomUser.objects.get(username=request.user.username).as_dict(),
        })
    return HttpResponse('test')
    # return JsonResponse({
    #     'user': {
    #         "name": "John Doe",
    #         "email": "john.doe@example.com",
    #         "password": "password123",
    #         "date_of_birth": "2000-01-01",  # Format as ISO date string
    #         "hobbies": [],  # Empty list for hobbies
    #         "friends": [],  # Empty list for friends
    #         "profile_picture": None,  # No profile picture
    #     }
    # })


def hobby_api_view(request: HttpRequest) -> HttpResponse:
    """Defining POST for new Hobby object."""
    if request.method == 'POST':
        POST = json.loads(request.body)
        new_hobby = Hobby.objects.create(
            name = POST['hobby_name'],
            description = POST['hobby_description']
        )
        return JsonResponse(new_hobby.as_dict())
    return JsonResponse ({})


def user_hobbies_api_view(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        POST = json.loads(request.body)
        # newHobby = UserHobby.objects.create(
            # user = user
            # hobby = POST
        # )
        print(POST['hobby_id'])

    return JsonResponse({
        'hobbies' : [user_hobby.hobby.as_dict() for user_hobby in UserHobby.objects.filter(user=id)],
    })