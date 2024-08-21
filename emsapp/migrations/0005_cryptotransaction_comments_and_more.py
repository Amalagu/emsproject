# Generated by Django 4.0.8 on 2024-07-08 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsapp', '0004_cryptotransaction_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptotransaction',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cryptotransaction',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='giftcardtransaction',
            name='card_country',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='giftcardtransaction',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giftcardtransaction',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cryptotransaction',
            name='timestamp',
            field=models.DateTimeField(auto_created=True),
        ),
        migrations.AlterField(
            model_name='giftcardtransaction',
            name='timestamp',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
