# Generated by Django 4.2.3 on 2023-07-31 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_remove_profile_following_profile_following_agencies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='model_class',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'A'), (1, 'B'), (2, 'C'), (3, 'Foreign Looking'), (4, 'Foreign'), (5, 'Indeterminate')], default=3, null=True, verbose_name='Model Class'),
        ),
    ]
