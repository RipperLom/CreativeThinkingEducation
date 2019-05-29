# Generated by Django 2.1.4 on 2019-01-03 11:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0006_auto_20190101_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuidName', models.CharField(max_length=50, unique=True, verbose_name='订单编号')),
                ('timeBegin', models.DateField(verbose_name='日期')),
                ('timeExpire', models.DateField(verbose_name='日期')),
                ('course', models.CharField(max_length=20, verbose_name='课程编号')),
                ('money', models.FloatField(verbose_name='金额')),
                ('voucher', models.CharField(max_length=200, verbose_name='凭证')),
                ('others', models.TextField(verbose_name='备注')),
                ('status', models.IntegerField(default=1)),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('addTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('modifyTime', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
                ('show', models.IntegerField(default=1)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.Client')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.Manager')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.Worker')),
            ],
        ),
    ]
