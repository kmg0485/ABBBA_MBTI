from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, ProfileSerializer, RecommendUserSerializer


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 추후 회원 탈퇴와 관련해 본인 버튼에만 탈퇴되도록 처리해야 합니다.    
    def delete(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if user:
            user.delete()
            return Response({"message":"지금까지 저희 서비스를 이용해 주셔서 감사합니다."}, status=status.HTTP_200_OK)
        return Response({"message":"이런... 탈퇴에 실패하셨습니다."}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 로그아웃은 추후 프론트에서 구현합니다.
# class Logout(APIView):
#     def post(self, request):
#         response = Response({
#             "message": "Logout!"
#         }, status=status.HTTP_202_ACCEPTED)
#         response.delete_cookie('refreshtoken')

#         return response


class ProfileView(APIView) :
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id) :
        user = get_object_or_404(User, id=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)



class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followers.all():
            you.followers.remove(me)
            return Response("Unfollow", status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response("Follow", status=status.HTTP_200_OK)


class UserRecommendView(APIView):
    def get(self, request):
        me = request.user
        recommend_user =User.objects.filter(mbti = me.mbti).exclude(id = me.id)
        print(recommend_user)
        serializer = RecommendUserSerializer(recommend_user,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        