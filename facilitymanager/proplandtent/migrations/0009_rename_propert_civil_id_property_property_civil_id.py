# Generated by Django 4.2.5 on 2023-09-26 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0008_alter_units_unit_bedrooms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='propert_civil_id',
            new_name='property_civil_id',
        ),
    ]