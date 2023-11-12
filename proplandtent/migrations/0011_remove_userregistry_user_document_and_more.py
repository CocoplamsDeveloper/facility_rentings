# Generated by Django 4.2.5 on 2023-11-12 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proplandtent', '0010_status_status_type_id_alter_status_status_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregistry',
            name='user_document',
        ),
        migrations.RemoveField(
            model_name='userregistry',
            name='user_image',
        ),
        migrations.RemoveField(
            model_name='userregistry',
            name='user_status',
        ),
        migrations.AddField(
            model_name='userregistry',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.status'),
        ),
        migrations.CreateModel(
            name='UserDocuments',
            fields=[
                ('document_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('document_name', models.CharField(max_length=1000)),
                ('document', models.FileField(upload_to='user_documents')),
                ('image', models.ImageField(upload_to='user_images')),
                ('document_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.userregistry')),
            ],
        ),
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('landlord_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('landlord_name', models.CharField(max_length=1000)),
                ('company_name', models.CharField(max_length=1000)),
                ('contact_name', models.CharField(max_length=1000)),
                ('contact_number', models.BigIntegerField(default=0)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=1000)),
                ('address', models.JSONField(default=dict)),
                ('remarks', models.CharField(max_length=1000)),
                ('landlord_type', models.CharField(max_length=200)),
                ('VAT_id', models.BigIntegerField(default=0)),
                ('bank_account_details', models.JSONField(default=dict)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proplandtent.userregistry')),
            ],
        ),
    ]