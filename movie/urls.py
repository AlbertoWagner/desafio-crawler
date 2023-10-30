from django.urls import path
from . import views

app_name = "movie"
urlpatterns = [
    path("", views.MoviesListView.as_view(), name="movie-list"),
    path(
        "export_movies/", views.ExportMoviesCsvView.as_view(), name="export-movies-csv"
    ),
    path(
        "export_movies_json/",
        views.ExportMoviesJsonView.as_view(),
        name="export-movies-json",
    ),
    path(
        "serializer/", views.MovieSerializerListView.as_view(), name="serializer-list"
    ),
]
