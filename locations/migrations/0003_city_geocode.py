# Generated by Django 4.0.5 on 2022-08-18 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_cityzone'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='geocode',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
