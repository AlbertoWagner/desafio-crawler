from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse

from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from movie.models import Movie
from movie.serializers import MovieSerializer


class MoviesListView(ListView):
    template_name = "movie/list.html"
    model = Movie
    paginate_by = 250


class ExportMoviesCsvView(View):
    def get(self, request):
        movies = Movie.objects.all()
        data = [
            [movie.title, movie.director, movie.year, movie.duration, movie.rating]
            for movie in movies
        ]
        import pandas as pd

        df = pd.DataFrame(
            data, columns=["Título", "Diretor", "Ano", "Duração", "Classificação"]
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="movie_data.csv"'
        df.to_csv(response, index=False)
        return response


class ExportMoviesJsonView(View):
    def get(self, request):
        movies = Movie.objects.all()
        movie_data = [
            {
                "Título": movie.title,
                "Diretor": movie.director,
                "Ano": movie.year,
                "Duração": movie.duration,
                "Classificação": str(movie.rating) + "º",
            }
            for movie in movies
        ]
        return JsonResponse(movie_data, safe=False)


class MovieSerializerListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = LimitOffsetPagination
