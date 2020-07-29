# Generated by Django 2.2 on 2020-07-29 04:20

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200725_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='/static/images/photo-of-lighthouse.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
