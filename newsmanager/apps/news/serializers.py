from authentication.serializers import UserSerializer
from django.utils import timezone
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

    def update(self, instance, validated_data):
        if instance.status == NewsPost.SCHEDULED:
            instance.status = NewsPost.DRAFT
        instance.save()
        return super().update(instance, validated_data)


class NewsPostPublishSerializer(serializers.ModelSerializer):
    schedule_date = serializers.DateTimeField(required=False)

    class Meta:
        model = NewsPost
        fields = ["status", "schedule_date"]
        read_only_fields = ["status"]

    def validate(self, data):
        if self.instance and self.instance.status == NewsPost.PUBLISHED:
            raise serializers.ValidationError(
                "Cannot schedule/publish a post that is already published."
            )
        return data

    def update(self, instance, validated_data):
        if validated_data.get("schedule_date") is None:
            instance.published_at = timezone.now()
            instance.status = NewsPost.PUBLISHED
        else:
            instance.published_at = validated_data["schedule_date"]
            instance.status = NewsPost.SCHEDULED
        instance.save()

        return instance

    def to_representation(self, instance):
        return NewsPostSerializer(instance).data