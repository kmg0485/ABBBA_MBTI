from movies import views
from django.urls import path

urlpatterns = [
    path('', views.MovieListView.as_view(), name="movie_list_view"),
    path('<int:movie_id>/', views.MovieDetailView.as_view(), name="movie_detail_view"),
    path('<int:movie_id>/likes/', views.MovieLikeView.as_view(), name="movie_like"),
    path('extract/', views.extract_MovieLikeView.as_view(), name="extract"),
    path('extractlist/<int:id>/', views.EctractMovieListView.as_view(), name="extractlist"),
]
