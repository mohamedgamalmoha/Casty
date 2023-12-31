# Generated by Django 4.2.3 on 2023-07-27 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0003_directoruser'),
        ('profiles', '0007_profileimage_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
        migrations.AddField(
            model_name='profile',
            name='following_agencies',
            field=models.ManyToManyField(blank=True, related_name='follower_agencies', to='agencies.agency', verbose_name='Following Agencies'),
        ),
        migrations.AddField(
            model_name='profile',
            name='following_models',
            field=models.ManyToManyField(blank=True, related_name='follower_models', to='profiles.profile', verbose_name='Following Models'),
        ),
    ]
