# Generated by Django 2.1.4 on 2018-12-30 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0004_expense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='uuidName',
            field=models.CharField(max_length=50, unique=True, verbose_name='单号'),
        ),
    ]
