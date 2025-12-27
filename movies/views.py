from django.shortcuts import render

def register(request):
    return render(request, 'auth/register.html')

def login(request):
    return render(request, 'auth/login.html')

def home(request):
    return render(request, 'index.html')

def admin_movie(request):
    return render(request, 'admin/index.html')

def manage_movies(request):
    return render(request, 'admin/manage_movie.html')
