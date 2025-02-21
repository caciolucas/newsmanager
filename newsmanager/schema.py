from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="News Manager API",
        default_version="v1",
        description="An API for managing news posts, verticals, tags, users, plans and subscriptions",
        contact=openapi.Contact(email="cclucas060901@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
