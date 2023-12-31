# Generated by Django 4.2.3 on 2023-07-19 18:52

import accounts.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import profiles.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('code', models.CharField(blank=True, max_length=5, null=True, verbose_name='Code')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'ordering': ['-create_at', '-update_at'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Public')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Bio')),
                ('gender', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], default=1, null=True, verbose_name='Gender')),
                ('race', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Caucasian / White'), (1, 'African / Black'), (2, 'Asian'), (3, 'Hispanic / Latinx'), (4, 'Native'), (5, 'American / Indigenous'), (6, 'Middle Eastern'), (7, 'Eastern'), (8, 'Pacific'), (9, 'Islander'), (10, 'Mixed / Multiracial'), (11, 'Other')], default=11, null=True, verbose_name='Race')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('phone_number_1', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone Number 1')),
                ('phone_number_2', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone Number 2')),
                ('city', models.CharField(blank=True, max_length=200, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, max_length=200, null=True, verbose_name='Country')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address')),
                ('travel_inboard', models.BooleanField(blank=True, help_text='Willingness to travel inboard / locally', null=True, verbose_name='Travel Inboard')),
                ('travel_outboard', models.BooleanField(blank=True, help_text='Willingness to travel outboard / globally', null=True, verbose_name='Travel outboard ')),
                ('days_away', models.PositiveSmallIntegerField(blank=True, help_text='How many days can you stay away from home?', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(365)], verbose_name='Days Away')),
                ('height', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(250)], verbose_name='Height')),
                ('weight', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(250)], verbose_name='Weight')),
                ('hair', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Black'), (1, 'Brown (Light, Medium, Dark)'), (2, 'Blonde (Light, Medium, Dark)'), (3, 'Red'), (4, 'Auburn'), (5, 'Brunette'), (6, 'Chestnut'), (7, 'Sandy'), (8, 'Gray / Silver'), (9, 'White'), (10, 'Bald'), (11, 'Other')], null=True, verbose_name='Hair Color')),
                ('eye', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Black'), (1, 'Brown'), (2, 'Blue'), (3, 'Green'), (4, 'Hazel'), (5, 'Gray'), (6, 'Amber'), (7, 'Violet'), (8, 'Other')], null=True, verbose_name='Eye Color')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Image')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='covers/', verbose_name='Cover Image')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('languages', models.ManyToManyField(to='profiles.language', verbose_name='Languages')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'ordering': ['-create_at', '-update_at'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
                'ordering': ['-create_at', '-update_at'],
            },
        ),
        migrations.CreateModel(
            name='ModelUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
            managers=[
                ('student', profiles.models.ModelUserManager()),
                ('objects', accounts.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Link')),
                ('is_active', models.BooleanField(blank=True, default=True, help_text='Designates whether this link is viewed at the profile', verbose_name='Active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='profiles.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Social Link',
                'verbose_name_plural': 'Social Links',
                'ordering': ('-create_at', '-update_at'),
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='profiles.skill', verbose_name='Skills'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='profiles.modeluser', verbose_name='User'),
        ),
        migrations.CreateModel(
            name='PreviousExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255, verbose_name='Company Name')),
                ('project_name', models.CharField(max_length=100, verbose_name='Project Name')),
                ('role', models.CharField(max_length=100, verbose_name='Role')),
                ('description', models.TextField(verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, help_text='If the project is ongoing, the end_date can be null', null=True, verbose_name='End Date')),
                ('is_active', models.BooleanField(blank=True, default=True, help_text='Designates whether experience is viewed at the profile', verbose_name='Active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Social Link',
                'verbose_name_plural': 'Social Links',
                'ordering': ('-create_at', '-update_at'),
            },
        ),
    ]
