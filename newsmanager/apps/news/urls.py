from rest_framework.routers import DefaultRouter

from news.views import NewsPostViewSet

router = DefaultRouter()

router.register("posts", NewsPostViewSet, basename="news-posts")


urlpatterns = [*router.urls]
