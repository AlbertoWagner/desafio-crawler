import json
from django.test import TestCase
from rest_framework.test import APIClient
from faker import Faker
from django.urls import reverse
from movie.models import Movie
from movie.serializers import MovieSerializer


class MovieTestCase(TestCase):
    def setUp(self):
        # Inicialização comum a todos os testes
        self.client = APIClient()
        self.list_url = reverse("movie:movie-list")
        self.serializer_list_url = reverse("movie:serializer-list")

        # Criação de dados de filme fictício para testes
        fake = Faker()
        self.title = fake.catch_phrase()
        self.movie_data = {
            "title": self.title,
            "year": fake.random_int(min=1900, max=2023),
            "duration": f"{fake.random_int(min=60, max=240)} minutos",
            "rating": fake.pyfloat(left_digits=1, right_digits=1, positive=True),
        }

        # Criação de um filme no banco de dados com os dados fictícios
        self.movie = Movie.objects.create(**self.movie_data)

        # Serialização do filme para comparação
        self.movie_serializer = MovieSerializer(instance=self.movie)

    def test_home_view(self):
        # Teste para verificar se a página inicial está acessível
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_list_movies(self):
        # Teste para verificar se a lista de filmes é acessível e contém o filme criado
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.movie.title in response.content.decode("utf-8"))

    def test_serializer_list_movies(self):
        # Teste para verificar se a lista serializada de filmes está acessível e corresponde ao filme criado
        response = self.client.get(self.serializer_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [self.movie_serializer.data])
