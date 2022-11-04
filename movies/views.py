from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from movies.models import Movie, MovieLike
from movies.serializers import MovieListSerializer, MovieDetailSerializer
from rest_framework import status
from django.core import serializers
from django.http import HttpResponse
from .machine import ExtractListMachine
import json


class MovieListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request) :
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MovieDetailView(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly ]
    
    def get(self, request, movie_id) :
        movie = get_object_or_404(Movie, movie_id=movie_id)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)
    

class MovieLikeView(APIView) :
    permission_classes = [IsAuthenticated]
    
    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, movie_id=movie_id)
        if request.user in movie.likes.all():
            movie.likes.remove(request.user)
            return Response("💔💔💔💔", status=status.HTTP_200_OK)
        else:
            movie.likes.add(request.user)
            return Response("💖💖💖💖", status=status.HTTP_200_OK)



class extract_MovieLikeView(APIView):

    def get(self, request):
        extract_MovieLike = MovieLike.objects.filter(id__isnull=False).order_by("user_id")
        extract_list = serializers.serialize('json', extract_MovieLike)
        return HttpResponse(extract_list, content_type="text/json-comment-filtered")
    
    
class EctractMovieListView(APIView):
    
    def get(request, self, id):
        print(request, id)
        machine = ExtractListMachine(request, id)
        return Response(machine)
