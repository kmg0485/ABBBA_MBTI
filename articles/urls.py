from articles import views
from django.urls import path

urlpatterns = [
    path('',views.ArticleView.as_view(), name = 'article_view'),
    path('<int:article_id>/',views.ArticleDetailView.as_view(), name='article_detail_view'),
    
]
