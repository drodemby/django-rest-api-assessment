"""View module for handling requests about Songs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist


class SongView(ViewSet):
    """Level up Songs view"""

    def create(self, request):
        """Handle GET requests for single Song

        Returns:
            Response -- JSON serialized Song
        """

        artist = Artist.objects.get(pk=request.data["artist"])
        
        song = Song.objects.create(
            title=request.data["title"],
            length=request.data["length"],
            album=request.data["album"],
            artist=artist,
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)
  
    def retrieve(self, request, pk):
      try:
        song = Song.objects.get(pk=pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)
      except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk):
        """Handle PUT requests for a Song

        Returns:
            Response -- Empty body with 204 status code
        """

        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.length = request.data["length"]
        song.album = request.data["album"]

        artist = Artist.objects.get(pk=request.data["artist"])
        song.artist = artist
        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to get all song

        Returns:
            Response -- JSON serialized list of song
        """
        song = Song.objects.all()
       
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for song
    """
    artist = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = ('id', 'title','artist', 'length', 'album', 'genres')
        depth = 1

    def get_genres(self, obj):
      genres = obj.genres.all()
      
      return [{'id': genres.genreId.id, 'description': genres.genreId.description} for genres in genres]
    
    def get_artist(self, obj):
      artist = obj.artist
      return [{'id': artist.id, 'name': artist.name,'age': artist.age, 'bio': artist.bio}]
