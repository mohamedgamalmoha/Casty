# Generated by Django 4.2.3 on 2023-08-27 17:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import djmoney.models.validators
import djmoney.money


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0012_alter_profile_cover_alter_profile_image_and_more'),
        ('agencies', '0008_alter_agencyimage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Film'), (1, 'Cinema'), (2, 'Fashion'), (3, 'Television'), (4, 'Commercials'), (5, 'Theater'), (6, 'Mixed'), (7, 'Other')], null=True, verbose_name='Industry')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('description', models.TextField(blank=True, help_text='Describe the role of the model', null=True, verbose_name='Description')),
                ('guidelines', models.TextField(blank=True, help_text='Provide guidelines for the models applying to this contract', null=True, verbose_name='Guidelines')),
                ('restrictions', models.TextField(blank=True, help_text='List any restrictions or things that are not allowed to be done', null=True, verbose_name='Restriction')),
                ('money_offer_currency', djmoney.models.fields.CurrencyField(choices=[('EGP', 'EGP £'), ('EUR', 'EUR €'), ('USD', 'USD $')], default='EGP', editable=False, max_length=3)),
                ('money_offer', djmoney.models.fields.MoneyField(decimal_places=4, max_digits=20, validators=[djmoney.models.validators.MinMoneyValidator(djmoney.money.Money(10, 'EGP')), djmoney.models.validators.MaxMoneyValidator(djmoney.money.Money(1000000, 'EGP'))], verbose_name='Money Offer')),
                ('start_at', models.DateTimeField(verbose_name='Start Date')),
                ('require_travel_inboard', models.BooleanField(blank=True, help_text='Does the location requires travel inboard / locally?', null=True, verbose_name='Requires Travel Inboard')),
                ('require_travel_outboard', models.BooleanField(blank=True, help_text='Does the location requires travel outboard / globally?', null=True, verbose_name='Requires Travel outboard')),
                ('num_of_days', models.PositiveSmallIntegerField(blank=True, help_text='How many days does the location last?', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(365)], verbose_name='Number Of Days')),
                ('city', models.CharField(blank=True, max_length=200, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, max_length=200, null=True, verbose_name='Country')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address')),
                ('num_of_models', models.PositiveSmallIntegerField(blank=True, help_text='How many models does the location need?', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Number Of Models')),
                ('gender', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], default=1, null=True, verbose_name='Gender')),
                ('race', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Caucasian / White'), (1, 'African / Black'), (2, 'Asian'), (3, 'Hispanic / Latinx'), (4, 'Native'), (5, 'American / Indigenous'), (6, 'Middle Eastern'), (7, 'Eastern'), (8, 'Pacific'), (9, 'Islander'), (10, 'Mixed / Multiracial'), (11, 'Other')], default=11, null=True, verbose_name='Race')),
                ('hair', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Black'), (1, 'Brown (Light, Medium, Dark)'), (2, 'Blonde (Light, Medium, Dark)'), (3, 'Red'), (4, 'Auburn'), (5, 'Brunette'), (6, 'Chestnut'), (7, 'Sandy'), (8, 'Gray / Silver'), (9, 'White'), (10, 'Bald'), (11, 'Other')], null=True, verbose_name='Hair Color')),
                ('eye', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Black'), (1, 'Brown'), (2, 'Blue'), (3, 'Green'), (4, 'Hazel'), (5, 'Gray'), (6, 'Amber'), (7, 'Violet'), (8, 'Other')], null=True, verbose_name='Eye Color')),
                ('age_min', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(4), django.core.validators.MaxValueValidator(100)], verbose_name='Minimum Age')),
                ('age_max', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(4), django.core.validators.MaxValueValidator(100)], verbose_name='Maximum Age')),
                ('height_min', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(250)], verbose_name='Minimum Height')),
                ('height_max', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(250)], verbose_name='Maximum Height')),
                ('weight_min', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(250)], verbose_name='Minimum Weight')),
                ('weight_max', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(250)], verbose_name='Maximum Weight')),
                ('is_active', models.BooleanField(blank=True, default=True, help_text='Designates whether contract is viewed for models', verbose_name='Active')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='agencies.agency', verbose_name='Agency')),
                ('languages', models.ManyToManyField(blank=True, to='profiles.language', verbose_name='Languages')),
                ('skills', models.ManyToManyField(blank=True, to='profiles.skill', verbose_name='Skills')),
            ],
            options={
                'verbose_name': 'Contract',
                'verbose_name_plural': 'Contracts',
                'ordering': ('-create_at', '-update_at'),
            },
        ),
        migrations.CreateModel(
            name='SoloContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Film'), (1, 'Cinema'), (2, 'Fashion'), (3, 'Television'), (4, 'Commercials'), (5, 'Theater'), (6, 'Mixed'), (7, 'Other')], null=True, verbose_name='Industry')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('description', models.TextField(blank=True, help_text='Describe the role of the model', null=True, verbose_name='Description')),
                ('guidelines', models.TextField(blank=True, help_text='Provide guidelines for the models applying to this contract', null=True, verbose_name='Guidelines')),
                ('restrictions', models.TextField(blank=True, help_text='List any restrictions or things that are not allowed to be done', null=True, verbose_name='Restriction')),
                ('money_offer_currency', djmoney.models.fields.CurrencyField(choices=[('EGP', 'EGP £'), ('EUR', 'EUR €'), ('USD', 'USD $')], default='EGP', editable=False, max_length=3)),
                ('money_offer', djmoney.models.fields.MoneyField(decimal_places=4, max_digits=20, validators=[djmoney.models.validators.MinMoneyValidator(djmoney.money.Money(10, 'EGP')), djmoney.models.validators.MaxMoneyValidator(djmoney.money.Money(1000000, 'EGP'))], verbose_name='Money Offer')),
                ('start_at', models.DateTimeField(verbose_name='Start Date')),
                ('require_travel_inboard', models.BooleanField(blank=True, help_text='Does the location requires travel inboard / locally?', null=True, verbose_name='Requires Travel Inboard')),
                ('require_travel_outboard', models.BooleanField(blank=True, help_text='Does the location requires travel outboard / globally?', null=True, verbose_name='Requires Travel outboard')),
                ('num_of_days', models.PositiveSmallIntegerField(blank=True, help_text='How many days does the location last?', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(365)], verbose_name='Number Of Days')),
                ('city', models.CharField(blank=True, max_length=200, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, max_length=200, null=True, verbose_name='Country')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address')),
                ('model_notes', models.TextField(blank=True, verbose_name='Director Notes')),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Accepted'), (3, 'Rejected'), (4, 'Other')], default=0, null=True, verbose_name='Status')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solo_contracts', to='agencies.agency', verbose_name='Agency')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='profiles.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Solo Contract',
                'verbose_name_plural': 'Solo Contracts',
                'ordering': ('-create_at', '-update_at'),
            },
        ),
        migrations.CreateModel(
            name='ContractRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_notes', models.TextField(blank=True, verbose_name='Director Notes')),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Accepted'), (3, 'Rejected'), (4, 'Other')], default=0, null=True, verbose_name='Status')),
                ('money_offer_currency', djmoney.models.fields.CurrencyField(choices=[('EGP', 'EGP £'), ('EUR', 'EUR €'), ('USD', 'USD $')], default='EGP', editable=False, max_length=3, null=True)),
                ('money_offer', djmoney.models.fields.MoneyField(blank=True, decimal_places=4, max_digits=20, null=True, validators=[djmoney.models.validators.MinMoneyValidator(djmoney.money.Money(10, 'EGP')), djmoney.models.validators.MaxMoneyValidator(djmoney.money.Money(1000000, 'EGP'))], verbose_name='Money Offer')),
                ('director_notes', models.TextField(blank=True, verbose_name='Director Notes')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='contracts.contract', verbose_name='Contract')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_requests', to='profiles.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Contract Request',
                'verbose_name_plural': 'Contract Requests',
                'ordering': ('-create_at', '-update_at'),
            },
        ),
    ]
