from django.urls import path
from .views import home, login, register, admin_movie, manage_movies, logout, detail_movie, delete_movie
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('detail/', detail_movie, name='detail_movie'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('adminmovie/', admin_movie, name='admin_movie'),
    path('managemovies/', manage_movies, name='manage_movies'),
    path('logout/', logout, name='logout'),
    path('delete_movie/<int:id>/', delete_movie, name='delete_movie'),
    path('managemovies/<int:id>/', manage_movies, name='movie_edit'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)