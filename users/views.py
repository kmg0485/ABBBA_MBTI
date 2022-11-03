from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from users.models import User
from users.serializers import ProfileSerializer


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class Logout(APIView):
    def post(self, request):
        response = Response({
            "message": "Logout!"
        }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('refreshtoken')

        return response
    
class ProfileView(APIView) :
    permission_classes = [IsAuthenticated]

    def get(self, request, id) :
        user = get_object_or_404(User, id=id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)