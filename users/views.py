from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from rest_framework.permissions import IsAuthenticated,  IsAuthenticatedOrReadOnly
from users.serializers import ProfileCreateSerializer

from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, ProfileSerializer, RecommendUserSerializer,UserSimpleSerializer,ProfileCreateSerializer
from movies.models import MovieLike


class UserView(APIView):  
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    def delete(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if user:
            user.delete()
            return Response({"message":"지금까지 저희 서비스를 이용해 주셔서 감사합니다."}, status=status.HTTP_200_OK)
        return Response({"message":"이런... 탈퇴에 실패하셨습니다."}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileView(APIView) :
    permission_classes = [IsAuthenticated]

    # 프로필 보기
    def get(self, request) :
        user = get_object_or_404(User, id=request.user.id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    
    # 프로필 입력
    def post(self,request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = ProfileCreateSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save(mbti=request.data["mbti"].upper())
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # 프로필 수정
    def put(self,request):
        user = get_object_or_404(User, id= request.user.id)

        if request.user == user:
            serializer = ProfileCreateSerializer(user, data = request.data)
            if serializer.is_valid(): 
                serializer.save(mbti=request.data["mbti"].upper())
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status = status.HTTP_403_FORBIDDEN)
        
class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me != you:
            if me in you.followers.all():
                you.followers.remove(me)
                return Response("Unfollow", status=status.HTTP_200_OK)
            else:
                you.followers.add(me)
                return Response("Follow", status=status.HTTP_200_OK)
        else: # 본인을 팔로우 하려고 하면 팔로우 동작을 하지 않고 메시지를 띄웁니다.
            return Response("본인을 팔로우할 수 없습니다.", status=status.HTTP_400_BAD_REQUEST)


class UserRecommendView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        me = request.user
        me_movie_like = MovieLike.objects.filter(user_id = me.id)
        me_movie_like = [x.movie for x in me_movie_like]
        print(me_movie_like)
        recommend_users = set()
        for movie in me_movie_like:
            for like_user in movie.movielike_set.all():
                recommend_users.add(like_user.user)

        me_followers = me.followings.filter(followers = me.id)
        for user in recommend_users.copy():
            for  follow_user in me_followers:
                if user.id == follow_user.id:

                    recommend_users.remove(user)              

        for user in recommend_users.copy():
            if user.mbti != me.mbti or user.id == me.id:
                recommend_users.remove(user)
            else:
                pass
        serializer = RecommendUserSerializer(me_movie_like,many=True)
        return Response(
            {
                'movies':serializer.data,
                'recommend_users': UserSimpleSerializer(recommend_users, many=True).data
             },
            status=status.HTTP_200_OK)