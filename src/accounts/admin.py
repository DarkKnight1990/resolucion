from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext as _

from accounts.forms.user_forms import (
    CustomUserCreationForm, CustomUserChangeForm
)
from accounts.models import (
    CustomUser, Organization, UserProfile
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('User Profile')
    fk_name = 'user'


class GroupInline(admin.TabularInline):
    model = CustomUser.groups.through


class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, GroupInline, )

    # forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        'email', 'first_name', 'last_name', 'date_joined', 'date_of_birth',
        'get_organization',
    )
    list_filter = ('is_staff', 'is_active', 'userprofile__organization__name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': (
            'first_name', 'last_name', 'date_joined', 'date_of_birth')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_superuser', 'is_staff')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'date_joined',
                'date_of_birth', 'password1', 'password2',
            )
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_organization(self, obj):
        return obj.userprofile.organization
    get_organization.short_description = _('Organization')


admin.site.register(CustomUser, CustomUserAdmin)
