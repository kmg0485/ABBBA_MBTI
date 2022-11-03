from rest_framework import serializers
from articles.models import Article

class ArticleSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Article
        fields = "__all__"

class ArticleCreateSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Article
        fields = ("pk","title","content","updated_at","created_at","user")

