from django.db import models
from users.models import User

class Movie(models.Model) :
    movie_id = models.IntegerField(primary_key = True, unique=True)
    title = models.CharField(max_length=100)
    poster = models.TextField()
    description = models.TextField(null=True)
    likes = models.ManyToManyField(User, related_name="movie_like")
    
    def __str__(self) :
        return str(self.title)
    
    