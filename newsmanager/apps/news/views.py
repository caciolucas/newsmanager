from django.db.models import Q
from rest_framework import permissions, viewsets

from news.models import NewsPost, NewsVerticals
from news.permissions import NewsPostPermission
from news.serializers import NewsPostSerializer


class NewsPostViewSet(viewsets.ModelViewSet):
    serializer_class = NewsPostSerializer
    queryset = NewsPost.objects.all()
    permission_classes = [permissions.IsAuthenticated, NewsPostPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_superuser:
            return NewsPost.objects.all().order_by("pk")
        elif user.groups.filter(pk=1).exists():
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
