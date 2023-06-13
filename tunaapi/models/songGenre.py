from django.db import models

from .song import Song
from .genre import Genre

class SongGenre(models.Model):

    songId = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='genres')
    genreId = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='songs')
