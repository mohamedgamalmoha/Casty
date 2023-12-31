# Generated by Django 4.2.3 on 2023-08-08 22:20

from django.db import migrations, models
import profiles.validators


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_alter_profile_cover_alter_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='profile/covers/', validators=[profiles.validators.FileSizeValidator(size_limit=5)], verbose_name='Cover Image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/images/', validators=[profiles.validators.FileSizeValidator(size_limit=5)], verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='profileimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/extra/', validators=[profiles.validators.FileSizeValidator(size_limit=5)], verbose_name='Image'),
        ),
    ]
