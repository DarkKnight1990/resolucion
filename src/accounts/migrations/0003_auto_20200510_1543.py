# Generated by Django 3.0 on 2020-05-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Organization Name'),
        ),
    ]