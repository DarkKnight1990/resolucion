from django import forms

from django_countries.widgets import CountrySelectWidget

from accounts.models import Organization


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['name', 'description', 'domain', 'countries', 'parent']
        widgets = {
            'country': CountrySelectWidget()
        }
