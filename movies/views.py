from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Movie
from django.core.exceptions import ValidationError
from .services.auth_service import AuthService
from .services.movie_service import MovieService
from .services.user_service import UserService

def register(request):
    if request.method == "POST":
        try:
            AuthService.register_user(
                full_name=request.POST.get("full_name"),
                email=request.POST.get("email"),
                password=request.POST.get("password"),
                password2=request.POST.get("password2")
            )

            messages.success(request, "Akun berhasil dibuat, silakan login")
            return redirect("login")

        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, "auth/register.html")

def login(request):
    if request.method == "POST":
        try:
            user = AuthService.login_user(
                email=request.POST.get("email"),
                password=request.POST.get("password")
            )

            auth_login(request, user)

            if user.is_staff or user.is_superuser:
                return redirect("/adminmovie")
            return redirect("/")

        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, "auth/login.html")

def home(request):
    all_movies = Movie.objects.all()
    recommended_movies = Movie.objects.oldest(limit=5)
    trending_movies = Movie.objects.latest(limit=5)

    return render(request, 'index.html', {
        "all_movies": all_movies,
        "recommended_movies": recommended_movies,
        "trending_movies": trending_movies
    })

def detail_movie(request, id):
    if not request.user.is_authenticated:
        return redirect("home")

    movie = Movie.objects.get(id=id)
    all_movies = Movie.objects.all()
    recommended_movies = Movie.objects.oldest(limit=5)
    trending_movies = Movie.objects.latest(limit=5)

    return render(request, 'detail_movie.html', {
        "movie": movie, 
        "all_movies": all_movies,
        "recommended_movies": recommended_movies,
        "trending_movies": trending_movies
    })

def admin_movie(request):
    if not request.user.is_staff:
        return redirect("home")

    search = request.GET.get("search_movie")

    movies = Movie.objects.all().order_by('-created_at')

    if search:
        movies = Movie.objects.search(search)

    total_movies = Movie.objects.count()
    total_users = User.objects.count()

    return render(request, 'admin/index.html', {
        "user": request.user,
        "movies": movies,
        "total_movies": total_movies,
        "total_users": total_users,
        "search": search
    })

def manage_movies(request, id=None):
    if not request.user.is_staff:
        return redirect("home")

    movie = None
    if id:
        movie = get_object_or_404(Movie, id=id)

    if request.method == "POST":
        try:
            if movie:
                MovieService.update_movie(movie, request.POST, request.FILES)
                messages.success(request, "Movie berhasil diupdate.")
            else:
                MovieService.create_movie(request.POST, request.FILES)
                messages.success(request, "Movie berhasil ditambahkan.")

            return redirect("admin_movie")

        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, "admin/manage_movie.html", {
        "movie": movie
    })

def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == "POST":
        movie.delete_with_poster()
        return redirect("admin_movie")


def user_list(request):
    if not request.user.is_staff:
        return redirect("home")

    users = User.objects.all().order_by("-date_joined")
    total_movies = Movie.objects.count()
    total_users = User.objects.count()

    return render(request, "admin/users.html", {
        'users': users,
        "total_movies": total_movies,
        "total_users": total_users
    })

def update_user(request, id):
    if not request.user.is_staff:
        return redirect("home")
    
    user = get_object_or_404(User, id= id)

    if request.method == "POST":
        UserService.update_user(id, request.POST)
        messages.success(request, "User berhasil di update")
        return redirect("user_list")
    
    return render(request, "admin/manage_user.html", {
        "user": user
    })


def delete_user(request, id):
    if not request.user.is_staff:
        return redirect("home")

    if request.method == "POST":
        UserService.delete_user(id)
        messages.success(request, "User deleted successfully")
        return redirect("user_list")


def logout(request):
    auth_logout(request)
    return redirect("home")

