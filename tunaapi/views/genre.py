"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, SongGenre

class GenreView(ViewSet):
    """Level up genres view"""

    def create(self, request):
        """Handle GET requests for single genre

        Returns:
            Response -- JSON serialized genre
        """

        genre = Genre.objects.create(
            description=request.data["description"],
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
  
    def retrieve(self, request, pk):
      try:
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
      except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk):
        """Handle PUT requests for a genre

        Returns:
            Response -- Empty body with 204 status code
        """

        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to get all genre

        Returns:
            Response -- JSON serialized list of genre
        """
        genre = Genre.objects.all()
        serializer = GenreSerializer(genre, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres"""

    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    artist = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()
    length = serializers.SerializerMethodField()

    class Meta:
        model = SongGenre
        fields = ('id', 'title', 'artist', 'album', 'length')

    def get_id(self, obj):
        return obj.songId.id

    def get_title(self, obj):
        return obj.songId.title

    def get_artist(self, obj):
        return obj.songId.artist.id

    def get_album(self, obj):
        return obj.songId.album

    def get_length(self, obj):
        return obj.songId.length   
                  
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    songs = SongGenreSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')
        depth = 1
