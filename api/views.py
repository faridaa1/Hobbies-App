from datetime import datetime
import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from .forms import SignupForm, LoginForm
from .models import CustomUser, Friendship, Hobby, UserHobby

URL = 'http://localhost:5173/'


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
                auth.login(request, user)  # logs in user and saves id in session
            return redirect('http://localhost:5173/profile/')
    else:
        form = SignupForm()

    return render(request, 'api/spa/signup.html', {"form": form})


def login(request: HttpRequest) -> HttpResponse:
    """View for user login (using ssr)"""
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('http://localhost:5173/profile/')
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    
    return render(request, 'api/spa/login.html', {"form": form})


def logout(request: HttpRequest) -> JsonResponse:
    auth.logout(request)
    return JsonResponse({'login page': 'http://localhost:8000/login/'})


def users_api_view(request: HttpRequest) -> JsonResponse:
    """Returns all users for a global store"""
    return JsonResponse({
        'users': [user.as_dict() for user in CustomUser.objects.all()],
    })


def hobbies_api_view(request: HttpRequest) -> JsonResponse:
    """Returning all hobbies for a global store"""
    return JsonResponse({
        'hobbies': [hobby.as_dict() for hobby in Hobby.objects.all()],
    })


def user_api_view(request: HttpRequest) -> JsonResponse:
    """Returning logged in user for a global store"""
    if (request.user.is_authenticated):
        return JsonResponse({
            'user': CustomUser.objects.get(username=request.user.username).as_dict(),
        })
    # redirect unauthenticated user to sign up page
    return JsonResponse({'Error' : 'Unauthorised user'}, status=401)


def check_password_api_view(request: HttpRequest, id: int, password: str) -> JsonResponse:
    if request == 'GET':
        user = get_object_or_404(CustomUser, pk=id)
        return JsonResponse({'match': user.check_password(password)})
    return JsonResponse({})

def profile_api_view(request: HttpRequest, id: int, field: str) -> JsonResponse:
    """Defining PUT request handling for profile data"""
    if request.method == 'PUT':
        if field == 'name':
            user.name = json.loads(request.body)
        elif field == 'email':
            user.email = json.loads(request.body) 
        elif field == 'dob':
            user.date_of_birth = datetime.strptime(json.loads(request.body), "%Y-%m-%d").date()
        elif field == 'password':
            user.set_password(json.loads(request.body)['newPassword'])
            user.save()
            # needed as django ends session
            user = authenticate(request, username=user.username, password=json.loads(request.body)['newPassword'])
            if user is not None:
                login(request, user) 
                return JsonResponse(user.as_dict())
        user.save()
        return JsonResponse(user.as_dict())
    elif request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=id)
        if field == 'pic': 
            user.profile_picture = request.FILES.get('profile_picture') 
        user.save()
        return JsonResponse(user.as_dict())

    return JsonResponse({})


def hobby_api_view(request: HttpRequest) -> JsonResponse:
    """Defining POST for Hobby object"""
    if request.method == 'POST':
        POST = json.loads(request.body)
        new_hobby = Hobby.objects.create(
            name = POST['hobby_name'],
            description = POST['hobby_description']
        )
        return JsonResponse(new_hobby.as_dict())
    return JsonResponse ({})


def user_hobbies_api_view(request: HttpRequest, id: int) -> JsonResponse:
    """Defining GET, POST, and DELETE handling for UserHobby"""
    if request.method == 'GET':
        user = CustomUser.objects.get(pk=id)
        return JsonResponse({
            'user_hobbies' : [user_hobby.as_dict() for user_hobby in UserHobby.objects.filter(user=user)],
        }) 
    elif request.method == 'POST':
        POST = json.loads(request.body)
        if POST['newHobby']['hobby_id'] != -1:
            # adding existing hobby
            newUserHobby = UserHobby.objects.create(
                user = CustomUser.objects.get(pk=id),
                hobby = Hobby.objects.get(pk=POST['newHobby']['hobby_id']),
                level = POST['newUserHobby']['level'],
                start_date = POST['newUserHobby']['start_date']
            )
        else:
            # creating hobby
            newHobby = Hobby.objects.create(
                name = POST['newHobby']['hobby_name'],
                description = POST['newHobby']['hobby_description']
            )
            newUserHobby = UserHobby.objects.create(
                user = CustomUser.objects.get(pk=id),
                hobby = newHobby,
                level = POST['newUserHobby']['level'],
                start_date = POST['newUserHobby']['start_date']
            )
        return JsonResponse(newUserHobby.as_dict())
    elif request.method == 'DELETE':
        id = id.split('&')
        user = CustomUser.objects.get(pk=id[0])
        hobby = Hobby.objects.get(pk=id[1])
        user_hobby = get_object_or_404(UserHobby, user=user, hobby=hobby)
        user_hobby.delete()
    return JsonResponse({})


def friendship_api_view(request: HttpRequest, id: int) -> JsonResponse:
    """Defining POST request handling for Friendship."""
    friendship = Friendship.objects.get(pk=id)
    if json.loads(request.body):
        # body is boolean related to whether friendship was accepted
        friendship.status = 'Accepted'
        friendship.save()
        return JsonResponse(friendship.as_dict(request.user.username))
    else:
        # if friendship is rejected, delete relationship
        friendship.delete()
        return JsonResponse({})