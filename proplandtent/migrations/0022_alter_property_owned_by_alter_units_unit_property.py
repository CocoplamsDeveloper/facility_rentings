# Generated by Django 4.2.5 on 2023-11-20 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0021_remove_property_property_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='owned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.userregistry'),
        ),
        migrations.AlterField(
            model_name='units',
            name='unit_property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.property'),
        ),
    ]