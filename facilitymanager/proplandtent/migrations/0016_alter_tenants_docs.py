# Generated by Django 4.2.5 on 2023-10-01 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0015_alter_property_property_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenants',
            name='docs',
            field=models.FileField(upload_to='tenants_documents'),
        ),
    ]