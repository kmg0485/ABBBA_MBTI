from movies import views
from django.urls import path

urlpatterns = [
    path('', views.MovieListView.as_view(), name="movie_list_view"),
    path('<int:movie_id>/', views.MovieDetailView.as_view(), name="movie_detail_view"),
    path('<int:movie_id>/likes/', views.MovieLikeView.as_view(), name="movie_like"),
]
