# Generated by Django 4.2.5 on 2023-09-20 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0003_alter_property_propert_civil_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='units',
            name='unit_bedrooms',
            field=models.CharField(default=0),
        ),
        migrations.AddField(
            model_name='units',
            name='unit_rent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
