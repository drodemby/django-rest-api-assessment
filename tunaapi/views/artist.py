"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Count
from tunaapi.models import Artist


class ArtistView(ViewSet):
    """Level up artists view"""

    def create(self, request):
        """Handle GET requests for single artist

        Returns:
            Response -- JSON serialized artist
        """

        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)
  
    def retrieve(self, request, pk):
      try:
        artist = Artist.objects.get(pk=pk)
        serializer = ArtistSerializer(artist)
        artist = Artist.objects.annotate(songs_count=Count('songs')).get(pk=pk)
        return Response(serializer.data)
      except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk):
        """Handle PUT requests for a artist

        Returns:
            Response -- Empty body with 204 status code
        """

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]


        artist.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to get all artist

        Returns:
            Response -- JSON serialized list of artist
        """
        artist = Artist.objects.all()
        serializer = ArtistSerializer(artist, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for Artist
    """
    songs_count = serializers.SerializerMethodField()
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'songs', 'songs_count')
        depth = 1
    
    def get_songs_count(self, obj):
        return obj.songs.count()
