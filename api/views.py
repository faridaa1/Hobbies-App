from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from .forms import SignupForm


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def signup(request: HttpRequest) -> HttpResponse:
    """View for user signup (using ssr)"""
    if request.method == "POST":
        # Create Signup form and populate w/ form data
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create user from this form
            return HttpResponse("USER VALID TODO: Create user in db")
    else:
        form = SignupForm()

    return render(request, 'api/spa/signup.html', {"form": form})