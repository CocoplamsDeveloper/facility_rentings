# Generated by Django 4.2.5 on 2023-09-21 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0004_units_unit_bedrooms_units_unit_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='units',
            name='unit_type',
            field=models.CharField(default='other'),
        ),
    ]