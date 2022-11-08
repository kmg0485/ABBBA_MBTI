from dataclasses import field, fields
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User
from movies.models import Movie, MovieLike

from articles.serializers import ArticleSerializer, CommentSerializer
from movies. serializers import MovieListSerializer

class ProfileCreateSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = ("email", "profile_img", "bio", "mbti")
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
    def update(self, validated_data):
        user = super().update(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod 
    def get_token(cls, user):
        token = super().get_token(user)
        token['nickname'] = user.nickname
        
        return token
        

class ProfileSerializer(serializers.ModelSerializer):
    followings = UserSerializer(many=True)  # 사용자가 팔로우하는 사람들
    followers = UserSerializer(many=True)  # 사용자를 팔로우하는 사람들

    article_set = ArticleSerializer(many=True) # 사용자가 작성한 게시글
    comment_set = CommentSerializer(many=True) # 사용자가 작성한 덧글들
    movie_set = MovieListSerializer(many=True) # 사용자가 좋아요 한 영화

    class Meta:
        model = User
        fields = '__all__'

# 유저 추천 시스템
class RecommendUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("title","poster","movie_id","likes")

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nickname","mbti","profile_img", "id")


