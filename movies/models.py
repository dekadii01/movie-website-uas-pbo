from django.db import models
import uuid
import os

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

    def __str__(self):
        return self.title