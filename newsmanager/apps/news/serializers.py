from authentication.serializers import UserSerializer
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from news.models import NewsPost

# Create your views here.


class NewsPostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = NewsPost
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "published_at",
            "deleted_at",
        ]
