from rest_framework import serializers
from articles.models import Article, Comment
class CommentSerializer(serializers.ModelSerializer):
     class Meta:
        model = Comment
        fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
     class Meta:
        model = Comment
        fields = ("content",)

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many= True)
    class Meta:
        model = Article
        fields = "__all__"

class ArticleCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        fields = ("pk","title","content","updated_at","created_at",)

