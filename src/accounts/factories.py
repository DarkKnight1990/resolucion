import factory

from faker import Factory

from accounts.models import CustomUser, Organization, UserProfile
from common.utils import generate_unique_slug

faker = Factory.create()


class OrganizationFactory(factory.DjangoModelFactory):

    class Meta:
        model = Organization
        django_get_or_create = ('slug',)

    name = factory.LazyAttribute(lambda o: faker.company())
    description = factory.LazyAttribute(lambda o: faker.text())
    slug = factory.LazyAttribute(
        lambda o: generate_unique_slug(Organization(), o.name)
    )
    domain = factory.LazyAttribute(lambda o: "www." + faker.domain_name())


class CustomUserFactory(factory.DjangoModelFactory):

    class Meta:
        model = CustomUser
        django_get_or_create = ('email',)

    email = factory.LazyAttribute(lambda o: faker.email())
    first_name = factory.LazyAttribute(lambda o: faker.first_name())
    last_name = factory.LazyAttribute(lambda o: faker.last_name)
    password = factory.LazyAttribute(lambda o: faker.password())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class UserProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserProfile
        django_get_or_create = ('user',)

    user = factory.SubFactory(CustomUserFactory)
    organization = factory.SubFactory(OrganizationFactory)
    contact_number = factory.LazyAttribute(lambda o: faker.msisdn())
