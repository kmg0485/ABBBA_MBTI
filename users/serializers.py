from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User
from movies.models import Movie
import re

from articles.serializers import ArticleSerializer, CommentSerializer
from movies. serializers import MovieListSerializer

class ProfileCreateSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = ("email", "profile_img", "bio", "mbti")
        

class UserSerializer(serializers.ModelSerializer):
    password_check= serializers.CharField(error_messages={'required':'비밀번호 확인까지 입력해 주세요.', 'blank':'비밀번호 확인까지 입력해 주세요.'}) 
    
    class Meta:
        model = User
        fields = ("nickname","password", "password_check")
        extra_kwargs = {
            "nickname" : {"error_messages":{
                "required":"닉네임 겸 아이디를 입력해 주세요.",
                "blank":"닉념임 겸 아이디를 입력해 주세요.",
                "invalid":"알맞은 형식의 닉네임을 입력해 주세요.",}},
            "password" : {"write_only":True, # password는 직렬화하지 않는다.
                          "error_messages":{
                "required":"비밀번호를 입력해 주세요.",
                "blank":"비밀번호를 입력해 주세요.",
                "invalid":"알맞은 형식의 비밀번호를 입력해 주세요."}},
        }
    
    def validate(self, validated_data) :
        nickname = validated_data.get("nickname")
        # 영문과 숫자, 특수문자는 사용 불가능하며, 2-10자 길이, 영문은 무조건 포함해야 한다.
        reg = r'^(?=.*[a-z])[a-z0-9]{2,10}$'
        password1 = validated_data.get("password")
        password2 = validated_data.get("password_check")
        
        # 닉네임 유효성 체크
        if not re.search(reg, nickname) :
            raise serializers.ValidationError(detail={"nickname":"닉네임은 소문자 알파벳과 숫자를 조합해 2~10글자 사이로 작성해 주세요! 특수문자는 사용 불가합니다."})
        
        # 비밀번호 유효성 체크
        if not re.search(reg, password1) :
            raise serializers.ValidationError(detail={"password":"비밀번호는 소문자 알파벳과 숫자를 조합해 2~10글자 사이로 작성해 주세요! 특수문자는 사용 불가합니다."})
        elif password1 != password2 :
            raise serializers.ValidationError(detail={"password":"동일한 비밀번호를 입력해 주세요."})
        
        return validated_data
        

    def create(self, validated_data):
        nickname = validated_data["nickname"]
        password = validated_data["password"]
        user = User(
            nickname=nickname,
            password = password
            )
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


