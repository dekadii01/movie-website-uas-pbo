from django.urls import path
from .views import home, login, register, admin_movie, manage_movies

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('adminmovie/', admin_movie, name='admin_movie'),
    path('managemovies/', manage_movies, name='manage_movies'),
]
