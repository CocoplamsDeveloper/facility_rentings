# Generated by Django 4.2.5 on 2023-11-13 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0012_landlord_nationality'),
    ]

    operations = [
        migrations.AddField(
            model_name='landlord',
            name='charges',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=15),
        ),
    ]