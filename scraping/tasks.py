import logging
from celery import shared_task

from movie.models import Movie
from scraping.scrapers import WebMovieScraper


@shared_task
def build_creat_and_update_movies():
    logger = logging.getLogger("db")
    import datetime

    data_hora_atual = datetime.datetime.now()
    data_hora_formatada = data_hora_atual.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Iniciando a extração de dados. {data_hora_formatada}")

    scraper = WebMovieScraper()
    try:
        movie_data = scraper.run()
    except Exception as e:
        logger.exception(f"Erro na extração de dados. {e}")

    logger.info("Fim da extração de dados.")

    movie_list = []
    movie_titles = []

    for data in movie_data:
        title = str(data["title"])
        movie = Movie(
            rating=data["rating"],
            title=data["title"],
            year=data["year"],
            duration=data["duration"],
            poster_url=data["poster_url"],
        )
        movie_list.append(movie)
        movie_titles.append(title)

    existing_movies = Movie.objects.filter(title__in=movie_titles)
    existing_movies_dict = {str(m.title): m for m in existing_movies}

    updated_movies = []
    created_movies = []

    for movie in movie_list:
        title = str(movie.title)
        if title in existing_movies_dict:
            existing_movie = existing_movies_dict[title]
            existing_movie.title = movie.title
            existing_movie.year = movie.year
            existing_movie.duration = movie.duration
            existing_movie.poster_url = movie.poster_url
            existing_movie.save()  # Atualizar o filme individualmente
            updated_movies.append(existing_movie)
        else:
            created_movies.append(movie)

    # Criar os novos filmes
    if created_movies:
        try:
            Movie.objects.bulk_create(created_movies)
        except Exception as e:
            logger.exception("Erro ao criar novos filmes: %s", str(e))

    logger.info(
        "Execução da função build_creat_and_update_movies() concluída com sucesso."
    )
