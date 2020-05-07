from django.utils.text import slugify


def generate_unique_slug(instance, value, slug_field_name='slug'):
    """
    return: unique slug for the instance class based on the value
    """
    origin_slug = slugify(value)
    numb = 1
    unique_slug = origin_slug + "-" + str(numb)

    Klass = instance.__class__
    while Klass.objects.filter(**{slug_field_name: unique_slug}).exists():
        numb += 1
        unique_slug = "{slug}-{num}".format(slug=origin_slug, num=str(numb))
    return unique_slug
