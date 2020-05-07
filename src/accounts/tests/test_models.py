from django.core import validators
from django.test import TestCase

from django_countries.fields import Country
from faker import Factory

from accounts.factories import OrganizationFactory
from accounts.models import Organization

fake = Factory.create()


class OrganizationModelTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.organization = OrganizationFactory()

    def test_organization_creation(self):
        self.assertTrue(isinstance(self.organization, Organization))
        self.assertEqual(str(self.organization), self.organization.name)
    
    def test_empty_organization(self):
        org = Organization()
        self.assertRaises(validators.ValidationError, org.full_clean)

    def test_organization_slug_cannot_be_common(self):
        current_org_count = Organization.objects.all().count()
        kwargs = {
            'name': fake.company(),
            'domain': fake.domain_name(),
            'slug': 'common-slug'
        }
        org1 = Organization.objects.create(**kwargs)
        self.assertEquals(current_org_count + 1, Organization.objects.all().count())
        org2 = Organization(**kwargs)
        self.assertRaises(validators.ValidationError, org2.full_clean)
