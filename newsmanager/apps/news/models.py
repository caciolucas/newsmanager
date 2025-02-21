from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_prose_editor.fields import ProseEditorField
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class NewsPost(BaseModel):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    STATUS_CHOICES = [
        (DRAFT, _("Draft")),
        (SCHEDULED, _("Scheduled")),
        (PUBLISHED, _("Published")),
    ]
    title = models.CharField(max_length=255, help_text="Title of the news post")
    sub_title = models.CharField(max_length=255, help_text="Subtitle of the news post")
    content = ProseEditorField(help_text="Content of the news post")
    image = models.ImageField(
        upload_to="news_images",
        blank=True,
        null=True,
        help_text="Banner image of the news post",
    )

    author = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="news_posts",
        help_text="Autor da notícia",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text="Status of the news post",
    )
    #! NOTE: Poderia fazer o controle de publicação com o campo published_at
    #! Talvez adicionar uma property verificando se published_at >= now
    published_at = models.DateTimeField(blank=True, null=True)
    verticals = models.ManyToManyField("NewsVerticals", related_name="posts")

    tags = TaggableManager(blank=True, through=UUIDTaggedItem)

    class Meta:
        db_table = "news_posts"
        verbose_name = "News Post"
        verbose_name_plural = "News Posts"

    def __str__(self):
        return self.title


class NewsVerticals(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "news_verticals"
        verbose_name = "News Verticals"
        verbose_name_plural = "News Verticals"

    def __str__(self):
        return self.name
