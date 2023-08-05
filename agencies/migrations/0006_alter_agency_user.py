# Generated by Django 4.2.3 on 2023-08-01 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0005_agencyimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agency', to='agencies.directoruser', verbose_name='User'),
        ),
    ]
