# Generated by Django 4.2.5 on 2023-11-13 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0011_remove_userregistry_user_document_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='landlord',
            name='nationality',
            field=models.CharField(default='None', max_length=500),
        ),
    ]
