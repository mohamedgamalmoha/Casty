# Generated by Django 4.2.3 on 2023-07-21 17:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('about', models.TextField(blank=True, null=True, verbose_name='About')),
                ('since', models.DateField(blank=True, null=True, verbose_name='Since')),
                ('is_authorized', models.BooleanField(blank=True, null=True, verbose_name='Is Authorized')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('phone_number_1', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone Number 1')),
                ('phone_number_2', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone Number 2')),
                ('city', models.CharField(blank=True, max_length=200, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, max_length=200, null=True, verbose_name='Country')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address')),
                ('latitude', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='Longitude')),
                ('service', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Models'), (1, 'Actors'), (2, 'Extras'), (3, 'Mixed')], null=True, verbose_name='Service')),
                ('industry', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Film'), (1, 'Cinema'), (2, 'Fashion'), (3, 'Television'), (4, 'Commercials'), (5, 'Theater'), (6, 'Mixed'), (7, 'Other')], null=True, verbose_name='Industry')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agency', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Agency',
                'verbose_name_plural': 'Agencies',
                'ordering': ['-create_at', '-update_at'],
            },
        ),
        migrations.CreateModel(
            name='PreviousWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Project Name')),
                ('client_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Client Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('success_story', models.TextField(blank=True, null=True, verbose_name='Success Story')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, help_text='If the project is ongoing, the end_date can be null', null=True, verbose_name='End Date')),
                ('is_active', models.BooleanField(blank=True, default=True, help_text='Designates whether experience is viewed at the profile', verbose_name='Active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='works', to='agencies.agency', verbose_name='Agency')),
            ],
            options={
                'verbose_name': 'Previous Work',
                'verbose_name_plural': 'Previous Works',
                'ordering': ('-create_at', '-update_at'),
            },
        ),
    ]
