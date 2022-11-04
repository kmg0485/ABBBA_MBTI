from django.db import models
from users.models import User

class Movie(models.Model) :
    movie_id = models.IntegerField(primary_key = True, unique=True)
    title = models.CharField(max_length=100)
    poster = models.TextField()
    description = models.TextField(null=True)

    likes = models.ManyToManyField(User, blank=True, through="MovieLike")
    
    def __str__(self) :
        return str(self.title)

class MovieLike(models.Model) :
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    love = models.IntegerField(default=True)

