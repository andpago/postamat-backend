from rest_framework import serializers, viewsets, pagination
from .models import Post

class FullPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'author', 'text', 'creation_date')


class PublicFeedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(public=True)
    serializer_class = FullPostSerializer

