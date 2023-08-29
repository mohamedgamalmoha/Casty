# Generated by Django 4.2.3 on 2023-08-29 09:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0012_alter_profile_cover_alter_profile_image_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('agencies', '0008_alter_agencyimage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Rate')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='Title')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Active')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='Object ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='agencies.agency', verbose_name='Agency')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Content Type')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='profiles.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Rate',
                'verbose_name_plural': 'Rates',
                'ordering': ('-create_at', '-update_at'),
                'indexes': [models.Index(fields=['content_type', 'object_id'], name='reviews_rat_content_db70d0_idx')],
                'unique_together': {('content_type', 'object_id')},
            },
        ),
    ]