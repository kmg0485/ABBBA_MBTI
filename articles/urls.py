from articles import views
from django.urls import path

urlpatterns = [
    path('',views.ArticleView.as_view(), name = 'article_view'),
    path('<int:article_id>/',views.ArticleDetailView.as_view(), name='article_detail_view'),
    path('<int:article_id>/comment/',views.CommentView.as_view(), name='comment_view'),
    path('<int:article_id>/comment/<int:comment_id>/',views.CommentDetailView.as_view(), name='comment_Detail_view'),
    path('<int:article_id>/like/', views.LikeView.as_view(), name='like_view'),
    path('search/', views.SearchView.as_view(), name="search_view"),
]
