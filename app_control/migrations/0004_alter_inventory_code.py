# Generated by Django 4.1.2 on 2022-12-29 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_control', '0003_invoice_invoiceitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='code',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
