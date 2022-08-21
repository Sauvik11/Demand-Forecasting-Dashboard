from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModelManager(models.Manager):
    def filter_active(self, *args, **kwargs):
        return super().filter(is_active=False, *args, **kwargs)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        _('active status'), default=True,
        help_text=_("Designates whether this item is active."))

    objects = BaseModelManager()

    class Meta:
        abstract = True
