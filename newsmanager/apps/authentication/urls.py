from django.urls import path

from authentication.views import DecoratedTokenObtainPairView, DecoratedTokenRefreshView

# Create your views here.

urlpatterns = [
    path("token/", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
]
