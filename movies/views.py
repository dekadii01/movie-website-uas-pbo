from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Movie

def register(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Password tidak cocok")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email sudah terdaftar")
            return redirect("register")

        user = User.objects.create_user(
            username=email, 
            email=email,
            password=password,
            first_name=full_name,
            is_staff= False,
            is_superuser= False
        )

        user.first_name = full_name
        user.save()

        messages.success(request, "Akun berhasil dibuat, silakan login")
        return redirect("login")

    return render(request, 'auth/register.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect("/adminmovie")
            else:
                return redirect("/")
        else:
            messages.error(request, "Email atau password salah.")

    return render(request, 'auth/login.html')

def home(request):
    return render(request, 'index.html')

def detail_movie(request):
    return render(request, 'detail_movie.html')

def admin_movie(request):
    if not request.user.is_staff:
        return redirect("home")

    movies = Movie.objects.all().order_by('-created_at')

    return render(request, 'admin/index.html', {
        "user": request.user,
        "movies": movies
    })

def manage_movies(request):
    if not request.user.is_staff:
        return redirect("home")

    if request.method == "POST":
        title = request.POST.get("title")
        year = request.POST.get("year")
        rating = request.POST.get("rating")
        genre = request.POST.get("genre")
        description = request.POST.get("description")
        poster = request.FILES.get("poster")

        Movie.objects.create(
            title=title,
            year=year,
            rating=rating,
            genre=genre,
            description=description,
            poster=poster
        )

        messages.success(request, "Movie berhasil ditambahkan.")
        return redirect("admin_movie")

    return render(request, 'admin/manage_movie.html')

def logout(request):
    auth_logout(request)
    return redirect("home")
