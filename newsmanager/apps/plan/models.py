from authentication.models import User
from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from news.models import NewsVerticals

# Create your models here.


class Plan(BaseModel):
    name = models.CharField(max_length=255)
    verticals = models.ManyToManyField(NewsVerticals, related_name="plans")

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")


class Subscription(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="subscriptions"
    )
    is_active = models.BooleanField(
        default=True, help_text="Is the subscription active?"
    )

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
