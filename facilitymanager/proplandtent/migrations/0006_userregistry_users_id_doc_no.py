# Generated by Django 4.2.5 on 2023-10-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0005_alter_units_unit_occupied_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistry',
            name='users_id_doc_no',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
