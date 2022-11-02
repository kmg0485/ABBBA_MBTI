from django.db import models
from users.models import User


class Article(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    likes = models.ManyToManyField(User, related_name="like_articles")

    def __str__(self):
        return str(self.title)