from rest_framework import serializers, viewsets, pagination

from core.serializers import UserSerializer
from .models import Post

class FullPostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ('title', 'author', 'text', 'creation_date', 'id')


class PublicFeedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(public=True)
    serializer_class = FullPostSerializer

