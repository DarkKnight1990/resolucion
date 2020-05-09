from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField

from accounts.managers import CustomUserManager
from common.models import AbstractTimeStamp


class Organization(AbstractTimeStamp):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    domain = models.CharField(max_length=100)
    countries = CountryField(multiple=True, blank=True)
    parent = models.ForeignKey(
        'self', verbose_name=_('parent organization'),
        blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')


class CustomUser(AbstractTimeStamp, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True
    )
    first_name = models.CharField(
        verbose_name=_('first name'), max_length=30, blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name=_('last name'), max_length=30, blank=True, null=True
    )
    date_joined = models.DateTimeField(
        verbose_name=_('date joined'), default=timezone.now
    )
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.first_name if self.first_name else self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`"
        return True

    @property
    def is_admin(self):
        return self.is_superuser


class UserProfile(AbstractTimeStamp):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        Organization, related_name='user_profiles',
        on_delete=models.CASCADE
    )
    contact_number = models.CharField(
        _('contact number'), max_length=15, null=True, blank=True
    )

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profile')
