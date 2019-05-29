# Generated by Django 2.1.4 on 2018-12-26 02:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('realName', models.CharField(max_length=20, verbose_name='姓名')),
                ('sex', models.IntegerField(default=1, verbose_name='性别')),
                ('tel', models.TextField(verbose_name='电话')),
                ('others', models.TextField(verbose_name='备注')),
                ('status', models.IntegerField(default=1)),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('addTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('modifyTime', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
                ('show', models.IntegerField(default=1)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.Manager')),
            ],
        ),
    ]
