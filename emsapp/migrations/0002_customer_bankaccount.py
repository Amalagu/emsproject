# Generated by Django 4.0.8 on 2024-07-01 12:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('emsapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=100)),
                ('othernames', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('mobile_number', models.CharField(max_length=15, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('joined_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=20)),
                ('account_type', models.CharField(max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to='emsapp.customer')),
            ],
        ),
    ]
