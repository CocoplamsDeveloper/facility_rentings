# Generated by Django 4.2.5 on 2023-10-16 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0002_userregistry_user_document_userregistry_user_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='built_year',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_civil_id',
            field=models.CharField(default='Not specified', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_description',
            field=models.TextField(default=None, max_length=500, null=True),
        ),
    ]
