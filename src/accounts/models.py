from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField

from common.models import AbstractTimeStamp


class Organization(AbstractTimeStamp):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    domain = models.CharField(max_length=100)
    countries = CountryField(multiple=True, blank=True)
    parent = models.ForeignKey(
        'self', verbose_name=_('Parent Organization'),
        blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
