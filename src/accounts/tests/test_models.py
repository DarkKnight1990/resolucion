from django.core import validators
from django.contrib.auth import get_user_model
from django.test import TestCase

from faker import Factory

from accounts.factories import (
    CustomUserFactory, OrganizationFactory, UserProfileFactory
)
from accounts.models import (
    Organization, UserProfile
)

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
        org_count = Organization.objects.all().count()
        kwargs = {
            'name': fake.company(),
            'domain': fake.domain_name(),
            'slug': 'common-slug'
        }
        Organization.objects.create(**kwargs)
        self.assertEquals(org_count + 1, Organization.objects.all().count())
        org2 = Organization(**kwargs)
        self.assertRaises(validators.ValidationError, org2.full_clean)


class CustomUserManagerTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normal@user.com', password='foo'
        )
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(ValueError):
            User.objects.create_user(email='')

        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com', password='foo'
        )
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_admin)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo',
                is_superuser=False
            )


class UserProfileModelTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.profile = UserProfileFactory()
        cls.user = CustomUserFactory()

    def test_user_profile_creation(self):
        self.assertTrue(isinstance(self.profile, UserProfile))

    def test_user_profile_has_user(self):
        with self.assertRaises(validators.ValidationError):
            profile = UserProfile()
            profile.full_clean()

    def test_user_profile_has_organization(self):
        with self.assertRaises(validators.ValidationError):
            profile = UserProfile(user=self.user)
            profile.full_clean()
