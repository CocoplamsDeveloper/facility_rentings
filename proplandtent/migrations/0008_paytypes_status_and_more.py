# Generated by Django 4.2.5 on 2023-11-06 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0007_property_deletedby_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayTypes',
            fields=[
                ('paytype_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('paytype_name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('status_type', models.BigIntegerField(default=0)),
                ('status', models.CharField(default='None')),
            ],
        ),
        migrations.RemoveField(
            model_name='tenancylease',
            name='tenancy_agreement',
        ),
        migrations.RemoveField(
            model_name='tenancylease',
            name='tenancy_status',
        ),
        migrations.AddField(
            model_name='tenancylease',
            name='deposit_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.CreateModel(
            name='tenancyDocuments',
            fields=[
                ('document_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('document_name', models.CharField(max_length=1000)),
                ('document', models.FileField(upload_to='tenancy_documents')),
                ('document_related_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.tenancylease')),
            ],
        ),
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('invoice_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('invoice_name', models.CharField(max_length=1000)),
                ('invoice_amount', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('remarks', models.CharField(default='None', max_length=1000)),
                ('payment_date', models.DateField()),
                ('created_on', models.DateTimeField()),
                ('discount', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('water_amount', models.BooleanField(default=False)),
                ('telephone_amount', models.BooleanField(default=False)),
                ('electricity_amount', models.BooleanField(default=False)),
                ('internet_connection', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.userregistry')),
                ('payment_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.paytypes')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.status')),
                ('tenancy_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.tenancylease')),
            ],
        ),
        migrations.AddField(
            model_name='tenancylease',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.status'),
        ),
    ]
