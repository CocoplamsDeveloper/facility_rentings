# Generated by Django 4.2.5 on 2023-11-18 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0015_landlord_subscription_end_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='units_numbers_start_range',
            new_name='total_units',
        ),
        migrations.RemoveField(
            model_name='property',
            name='bathrooms_per_unit',
        ),
        migrations.RemoveField(
            model_name='property',
            name='parking_areas',
        ),
        migrations.AddField(
            model_name='property',
            name='construction_cost',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='property',
            name='zip_code',
            field=models.BigIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='PropertyDocuments',
            fields=[
                ('document_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('document_name', models.CharField(max_length=1000)),
                ('image', models.ImageField(upload_to='property_images')),
                ('document', models.FileField(upload_to='property_documents')),
                ('document_property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.property')),
            ],
        ),
        migrations.CreateModel(
            name='Facilities',
            fields=[
                ('facility_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=500)),
                ('included', models.BooleanField(default=False)),
                ('facility_cost', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('property_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.property')),
            ],
        ),
    ]