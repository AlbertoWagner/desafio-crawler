from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name="Título")
    year = models.CharField(max_length=4)
    duration = models.CharField(max_length=255)
    poster_url = models.URLField(blank=True, null=True, verbose_name="URL do Pôster")
    rating = models.IntegerField(blank=True, null=True, verbose_name="Classificação")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Filme"
        verbose_name_plural = "Filmes"
