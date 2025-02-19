from django.contrib import admin

from news.models import NewsPost, NewsVerticals

# Register your models here.


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ["title", "sub_title", "published_at"]
    search_fields = ["title", "sub_title"]
    list_filter = ["published_at"]
    date_hierarchy = "published_at"
    readonly_fields = ["published_at", "created_at", "updated_at", "deleted_at"]
    filter_horizontal = ("verticals",)


admin.site.register(NewsVerticals)
