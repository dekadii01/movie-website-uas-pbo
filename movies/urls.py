from django.urls import path
from .views import home, login, register, admin_movie, manage_movies, logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('adminmovie/', admin_movie, name='admin_movie'),
    path('managemovies/', manage_movies, name='manage_movies'),
    path('logout/', logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)