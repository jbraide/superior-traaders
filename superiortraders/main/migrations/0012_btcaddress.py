# Generated by Django 2.2 on 2020-07-25 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_withdraw'),
    ]

    operations = [
        migrations.CreateModel(
            name='BTCAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=40)),
            ],
        ),
    ]
