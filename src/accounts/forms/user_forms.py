from django import forms
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField
)
from django.utils.translation import ugettext as _

from accounts.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    """
    A form for creating new users.
    """

    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_('Confirm Password'), widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'date_joined', 'date_of_birth'
        )

    def clean_password2(self):
        # check the two password entries matches
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField(
        label=(_("Password")),
        help_text=(_("""Raw passwords are not stored, so there is no way to see
                    this user's password, but you can change the password
                    using <a href=\"../password/\">this form</a>."""))
    )

    class Meta:
        model = CustomUser
        fields = (
            'email', 'password', 'first_name', 'last_name', 'date_joined',
            'date_of_birth'
        )

    def clean_password(self):
        return self.initial['password']
