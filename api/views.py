from datetime import datetime
import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from .forms import SignupForm, LoginForm
from .models import CustomUser, Friendship, Hobby, UserHobby
from datetime import date


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
            return redirect('/profile/')
    else:
        form = SignupForm()

    return render(request, 'api/spa/signup.html', {"form": form})


def login(request: HttpRequest) -> HttpResponse:
    """View for user login (using ssr)"""
    return render(request, 'templates/api/spa/login.html')

    if request.method == "POST":
        form: LoginForm = LoginForm(request.POST)

        if form.is_valid():
            email: str = form.cleaned_data['email']
            password: str = form.cleaned_data['password']
            user: CustomUser | None = authenticate(request, username=email, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/profile/')
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form: LoginForm = LoginForm()
    
    return render(request, 'api/spa/login.html', {"form": form})


def logout(request: HttpRequest) -> JsonResponse:
    """Handling user logout"""
    try:
        auth.logout(request)
    except:
        pass
    return JsonResponse({'login page': '/login/'})


def users_api_view(request: HttpRequest) -> JsonResponse:
    """Returns all users for a global store"""
    try:
        return JsonResponse({
            'users': [user.as_dict() for user in CustomUser.objects.all()],
        })
    except: 
        return JsonResponse({
                'users': [],
        })


def hobbies_api_view(request: HttpRequest) -> JsonResponse:
    """Returning all hobbies for a global store"""
    try:
        return JsonResponse({
            'hobbies': [hobby.as_dict() for hobby in Hobby.objects.all()],
        })
    except: 
        return JsonResponse({
            'hobbies': [],
        })
    
    
def all_users_api_view(request: HttpRequest) -> JsonResponse:
    """API view to return all users with calculated age."""
    def calculate_age(dob):
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    users = CustomUser.objects.filter(is_active=True).exclude(is_staff=True)  # Exclude staff users
    user_data = [
        {
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
            "profile_picture": user.profile_picture.url if user.profile_picture else None,
            "age": calculate_age(user.date_of_birth),
        }
        for user in users
    ]
    return JsonResponse(user_data, safe=False)


def user_api_view(request: HttpRequest) -> JsonResponse:
    """Returning logged in user for a global store"""
    if (request.user.is_authenticated):
        return JsonResponse({
            'user': CustomUser.objects.get(username=request.user.username).as_dict(),
        })
    # redirect unauthenticated user to login page
    form: LoginForm = LoginForm()
    return render(request, 'api/spa/login.html', {"form": form})
    # return JsonResponse({'user' : '/login/'})


def check_password_api_view(request: HttpRequest, id: int, password: str) -> JsonResponse:
    if request.method == 'GET':
        try:
            user: CustomUser = CustomUser.objects.get(pk=id)
            if user.check_password(password):
                return JsonResponse({'match': True})
        except:
            pass
    return JsonResponse({'match': False})


def profile_api_view(request: HttpRequest, id: int, field: str) -> JsonResponse:
    """Defining PUT and POST request handling for profile data"""
    try:
        user: CustomUser = CustomUser.objects.get(pk=id)
        if request.method == 'PUT':
            if field == 'name':
                user.name = json.loads(request.body)
            elif field == 'email':
                user.email = json.loads(request.body) 
                user.username = json.loads(request.body)
            elif field == 'dob':
                user.date_of_birth = datetime.strptime(json.loads(request.body), "%Y-%m-%d").date()
            elif field == 'password':
                user.set_password(json.loads(request.body)['newPassword'])
                user.save()
                # needed as django ends session
                user: CustomUser | None = authenticate(request, username=user.username, password=json.loads(request.body)['newPassword'])
                if user is not None:
                    auth.login(request, user) 
                    return JsonResponse(user.as_dict())
            user.save()
            return JsonResponse(user.as_dict())
        elif request.method == 'POST':
            if field == 'pic': 
                user.profile_picture = request.FILES.get('profile_picture') 
            user.save()
            return JsonResponse(user.as_dict())
    except:
        pass
    return JsonResponse({})


def user_hobbies_api_view(request: HttpRequest, id: int) -> JsonResponse:
    """Defining GET, POST, and DELETE handling for UserHobby"""
    try:
        if request.method == 'GET':
            user: CustomUser = CustomUser.objects.get(pk=id)
            return JsonResponse({
                'user_hobbies' : [user_hobby.as_dict() for user_hobby in UserHobby.objects.filter(user=user)],
            }) 
        elif request.method == 'POST':
            POST: dict[str, str] = json.loads(request.body)
            if POST['newHobby']['hobby_id'] != -1:
                # adding existing hobby
                user1: CustomUser = CustomUser.objects.get(pk=id)
                newUserHobby: UserHobby = UserHobby.objects.create(
                    user = user1,
                    hobby = Hobby.objects.get(pk=POST['newHobby']['hobby_id']),
                    level = POST['newUserHobby']['level'],
                    start_date = POST['newUserHobby']['start_date']
                )
            else:
                user1: CustomUser = CustomUser.objects.get(pk=id)
                # creating hobby
                newHobby: Hobby = Hobby.objects.create(
                    name = POST['newHobby']['hobby_name'],
                    description = POST['newHobby']['hobby_description']
                )
                newUserHobby: UserHobby = UserHobby.objects.create(
                    user = user1,
                    hobby = newHobby,
                    level = POST['newUserHobby']['level'],
                    start_date = POST['newUserHobby']['start_date']
                )
            return JsonResponse({'user_hobbies' : newUserHobby.as_dict()})
        elif request.method == 'DELETE':
            id: list[str] = id.split('&')
            user1: CustomUser = CustomUser.objects.get(pk=id[0])
            hobby1: Hobby = Hobby.objects.get(pk=id[1])
            user_hobby: UserHobby = UserHobby.objects.get(user=user1, hobby=hobby1)
            user_hobby.delete()
    except:
        if request.method == 'DELETE':
            return JsonResponse({'user_hobbies': []}, status=500)
        pass
    return JsonResponse({'user_hobbies': []})


def friendship_api_view(request: HttpRequest, from_id: int, to_username: str) -> JsonResponse:
    """Defining POST request handling for Friendship."""
    try:
        from_user = CustomUser.objects.get(pk=from_id)
        to_user = CustomUser.objects.get(username=to_username)
        if request.method == 'POST':
            friendship = Friendship.objects.create(user1=from_user, user2=to_user,status='Pending')
            return JsonResponse({'friendship': friendship.as_dict(current_user=from_user)})
        else:
            return JsonResponse({}, status=405)
    except:
        return JsonResponse({}, status=500)
    
    
def friendship_update_api_view(request: HttpRequest, id: int) -> JsonResponse:
    """Defines DELETE and PUT request handling for a friendship"""
    try:
        friendship = Friendship.objects.get(pk=id)
        if request.method == 'DELETE':
            friendship.delete()
            return JsonResponse({}, status=204)
        elif request.method == 'PUT':
            # Update friendship status
            if json.loads(request.body):
                # body is boolean related to whether friendship was accepted
                friendship.status = 'Accepted'
                friendship.save()
                return JsonResponse(friendship.as_dict(request.user.username))
            else:
                # if friendship is rejected, delete relationship
                friendship.delete()
                return JsonResponse({})
        else:
            return JsonResponse({}, status=405)
    except:
        return JsonResponse({}, status=500)