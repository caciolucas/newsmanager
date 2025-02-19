from rest_framework import permissions

from news.admin import NewsPost


class NewsPostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.has_perm("news.add_newspost")
        return True

    def has_object_permission(self, request, view, obj: NewsPost):
        if request.user.is_admin or request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return obj.verticals.filter(
                plans__subscriptions__user=request.user,
                plans__subscriptions__is_active=True,
            ).exists() or (obj.author == request.user)

        if request.method in ["PUT", "PATCH"]:
            return obj.author == request.user and request.user.has_perm(
                "news.change_newspost"
            )

        if request.method == "DELETE":
            return obj.author == request.user and request.user.has_perm(
                "news.delete_newspost"
            )

        return False
