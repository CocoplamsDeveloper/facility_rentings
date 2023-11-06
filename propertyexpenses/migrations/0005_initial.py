# Generated by Django 4.2.5 on 2023-11-06 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proplandtent', '0008_paytypes_status_and_more'),
        ('propertyexpenses', '0004_remove_payments_invoice_id_remove_payments_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('payment_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('transaction_id', models.CharField(default='askj3763', max_length=1000)),
                ('amount', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('created_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField()),
                ('invoice_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.invoices')),
                ('payment_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.paytypes')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.status')),
            ],
        ),
    ]
