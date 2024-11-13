from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def signup_spa(request: HttpRequest) -> HttpResponse:
    """View for user signup (using ssr)"""
    return render(request, 'api/spa/signup.html', {})