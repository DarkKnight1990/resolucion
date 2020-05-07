import factory

from django_countries.fields import Country
from django_countries.tests.models import MultiCountry
from faker import Factory

from accounts.models import Organization
from common.utils import generate_unique_slug

faker = Factory.create()


class OrganizationFactory(factory.DjangoModelFactory):

    class Meta:
        model = Organization
        django_get_or_create = ('slug',)
    
    name        = factory.LazyAttribute(lambda o: faker.company())
    description = factory.LazyAttribute(lambda o: faker.text())
    slug        = factory.LazyAttribute(lambda o: generate_unique_slug(Organization(), o.name))
    domain      = factory.LazyAttribute(lambda o: "www." + faker.domain_name())
