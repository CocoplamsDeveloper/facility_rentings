# Generated by Django 4.2.5 on 2023-11-05 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proplandtent', '0007_property_deletedby_user'),
        ('propertyexpenses', '0002_delete_invoices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('invoice_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('invoice_amount', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('remarks', models.CharField(default='None', max_length=1000)),
                ('payment_date', models.DateField()),
                ('created_on', models.DateTimeField()),
                ('discount', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='proplandtent.userregistry')),
                ('related_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.units')),
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
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('payment_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('transaction_id', models.CharField(default='askj3763', max_length=1000)),
                ('payment_type', models.CharField(default='None', max_length=250)),
                ('amount', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('created_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField()),
                ('invoice_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='propertyexpenses.invoices')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='propertyexpenses.status')),
            ],
        ),
        migrations.AddField(
            model_name='invoices',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='propertyexpenses.status'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='tenant_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.userregistry'),
        ),
    ]
