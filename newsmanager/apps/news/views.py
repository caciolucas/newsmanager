from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from news.models import NewsPost, NewsVerticals
from news.permissions import NewsPostPermission
from news.serializers import NewsPostPublishSerializer, NewsPostSerializer


class NewsPostViewSet(viewsets.ModelViewSet):
    serializer_class = NewsPostSerializer
    queryset = NewsPost.objects.all()
    permission_classes = [permissions.IsAuthenticated, NewsPostPermission]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "create", "update", "partial_update"]:
            return NewsPostSerializer
        elif self.action == "publish":
            return NewsPostPublishSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return NewsPost.objects.all().order_by("pk")
        elif user.groups.filter(name="Editor").exists():
            return NewsPost.objects.filter(author=user).order_by("pk")
        else:
            active_verticals = NewsVerticals.objects.filter(
                plans__subscriptions__user=user, plans__subscriptions__is_active=True
            )
            return (
                NewsPost.objects.filter(verticals__in=active_verticals)
                .distinct()
                .order_by("pk")
            )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @swagger_auto_schema(request_body=None, responses={200: NewsPostSerializer})
    @action(detail=True, methods=["POST"])
    def publish(self, request, pk=None):
        newspost = self.get_object()
        serializer = self.get_serializer(newspost, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
