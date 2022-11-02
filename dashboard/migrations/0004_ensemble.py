# Generated by Django 3.2.15 on 2022-11-01 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_corr_dates_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ensemble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Final_forecast', models.FloatField(blank=True, null=True)),
                ('ID', models.CharField(blank=True, max_length=25, null=True)),
                ('Type', models.CharField(blank=True, max_length=25, null=True)),
                ('block', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
