from movies.models import Movie
from django.core.exceptions import ValidationError

class MovieService:

    @staticmethod
    def create_movie(data, files):
        title = data.get("title")
        year = data.get("year")
        rating = data.get("rating")
        genre = data.get("genre")
        description = data.get("description")
        poster = files.get("poster")

        if not title:
            raise ValidationError("Judul film wajib diisi")

        return Movie.objects.create(
            title=title,
            year=year,
            rating=rating,
            genre=genre,
            description=description,
            poster=poster
        )

    @staticmethod
    def update_movie(movie, data, files):
        movie.title = data.get("title")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre = data.get("genre")
        movie.description = data.get("description")

        poster = files.get("poster")
        if poster:
            movie.poster = poster

        movie.save()
        return movie
