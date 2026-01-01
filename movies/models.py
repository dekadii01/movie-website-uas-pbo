from django.db import models
import uuid
import os
from django.db.models import Q

class MovieQuerySet(models.QuerySet):
    def latest(self, limit=5):
        return self.order_by('-created_at')[:limit]

    def oldest(self, limit=5):
        return self.order_by('created_at')[:limit]

    def search(self, keyword):
        return self.filter(
            Q(title__icontains=keyword) |
            Q(genre__icontains=keyword) |
            Q(year__icontains=keyword)
        )

class MovieManager(models.Manager):
    def get_queryset(self):
        return MovieQuerySet(self.model, using=self._db)

    def latest(self, limit=5):
        return self.get_queryset().latest(limit)

    def oldest(self, limit=5):
        return self.get_queryset().oldest(limit)

    def search(self, keyword):
        return self.get_queryset().search(keyword)

def poster_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f"posters/{filename}"

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    genre = models.CharField(max_length=50)
    description = models.TextField()
    poster = models.ImageField(upload_to=poster_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "movies"

    objects = MovieManager()

    def __str__(self):
        return self.title

    def delete_with_poster(self):
        if self.poster:
            self.poster.delete(save=False)
        self.delete()