# Generated by Django 2.1.4 on 2019-01-01 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0005_auto_20181230_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='voucher',
            field=models.CharField(max_length=200, verbose_name='凭证'),
        ),
    ]
