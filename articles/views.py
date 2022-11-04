from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.serializers import ArticleSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer
from .models import Article, Comment
from users.models import User
# Create your views here.

class ArticleView(APIView):

    def get(self, request):

        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):

        serializer = ArticleCreateSerializer(data = request.data)

        if serializer.is_valid():
            
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):

    def get(self, request, article_id):
        article = get_object_or_404(Article,id= article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status = status.HTTP_200_OK)
        
    def put(self,request,article_id):

        article = get_object_or_404(Article, id= article_id)

        if request.user == article.user:
            serializer = ArticleCreateSerializer(article, data = request.data)
            if serializer.is_valid(): 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status = status.HTTP_403_FORBIDDEN)


        
    def delete(self,request,article_id):

        article = get_object_or_404(Article, id= article_id)
        
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status = status.HTTP_403_FORBIDDEN)

class CommentView(APIView):
    
    def get(self, request,article_id):
        article = Article.objects.get(id= article_id)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,article_id):
        serializer = CommentCreateSerializer(data = request.data)
        if serializer.is_valid():
            
            serializer.save(user=request.user, article_id = article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):

    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id= comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data = request.data)
            if serializer.is_valid(): 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status = status.HTTP_403_FORBIDDEN)

    
    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment,id= comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status = status.HTTP_403_FORBIDDEN)

    
class LikeView(APIView):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)

        

class SearchView(APIView) :
    def get(self, request) :
        search_word = request.GET.get("search_word")
        articles = []

        users = User.objects.filter(mbti__contains=search_word)
        for user in users :
            user_articles = user.article_set.all()
            articles += user_articles
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
