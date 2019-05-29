from django.db import models
from django.utils import timezone
# Create your models here.
class Manager(models.Model):
    '''管理所有客户、工人、订单的信息
    超级管理，能够对所有信息进行创建修改
    一般管理，能够对所有未提交的信息进行创建和修改
    '''
    id = models.AutoField(primary_key=True)
    # 自增主键
    name = models.CharField('姓名', max_length=20, null=False)
    # 姓名
    password = models.CharField('密码', max_length=20, null=False)
    # 密码
    createTime = models.DateTimeField('创建日期', auto_now_add=True)
    addTime = models.DateTimeField('保存日期', default=timezone.now)
    modifyTime = models.DateTimeField('最后修改日期', auto_now=True)
    # 创建时间
    superManager = models.IntegerField(default=1)
    # 超级管理员为0，一般管理员默认为1
    show = models.IntegerField(default=1)
    # 1为未删除，0为已删除

class Notice(models.Model):
    '''公告信息
    '''
    id = models.AutoField(primary_key=True)
    # 自增主键
    content = models.TextField(null=False)
    # 存储内容
    createTime = models.DateTimeField('创建日期', auto_now_add=True)
    addTime = models.DateTimeField('保存日期', default=timezone.now)
    modifyTime = models.DateTimeField('最后修改日期', auto_now=True)
    # 创建时间

class Client(models.Model):
    '''客户姓名、年龄、联系方式
    '''
    id = models.AutoField(primary_key=True)
    # 自增主键
    name = models.CharField('用户名', max_length=20, null=False, unique=True)
    # 用户名
    realName = models.CharField('姓名', max_length=20, null=False)
    # 姓名
    sex = models.IntegerField('性别', default=1)
    # 性别
    age = models.IntegerField('年龄')
    # 年龄
    tel = models.TextField('电话')
    # 电话
    address = models.TextField('地址')
    # 地址
    kindergarten = models.CharField(max_length=20)
    primarySchool = models.CharField(max_length=20)
    junior = models.CharField(max_length=20)
    senior = models.CharField(max_length=20)
    # 学校信息
    others = models.TextField('备注家长信息')
    # 备注家长信息
    status = models.IntegerField(default=1)
    # 1 未提交
    # 2 修改中
    # 3 提交未审核
    # 4 申请修改中
    # 5 审核通过
    createTime = models.DateTimeField('创建日期', auto_now_add=True)
    addTime = models.DateTimeField('保存日期', default=timezone.now)
    modifyTime = models.DateTimeField('最后修改日期', auto_now=True)
    # 创建时间
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    # 外键
    show = models.IntegerField(default=1)

class Worker(models.Model):
    '''工人姓名、年龄、联系方式
    '''
    id = models.AutoField(primary_key=True)
    # 自增主键
    name = models.CharField('用户名', max_length=20, null=False, unique=True)
    # 用户名
    realName = models.CharField('姓名', max_length=20, null=False)
    # 姓名
    sex = models.IntegerField('性别', default=1)
    # 性别
    subject = models.CharField('学科', max_length=20, default='科学')
    # 课程
    tel = models.TextField('电话')
    # 电话
    others = models.TextField('备注')
    # 备注
    status = models.IntegerField(default=1)
    # 1 未提交
    # 2 修改中
    # 3 提交未审核
    # 4 申请修改中
    # 5 审核通过
    createTime = models.DateTimeField('创建日期', auto_now_add=True)
    addTime = models.DateTimeField('保存日期', default=timezone.now)
    modifyTime = models.DateTimeField('最后修改日期', auto_now=True)
    # 创建时间
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    # 外键
    show = models.IntegerField(default=1)

class Expense(models.Model):
    '''支出的名称、日期、金额、收款人、负责人、凭证
    '''
    id = models.AutoField(primary_key=True)
    # 自增主键
    uuidName = models.CharField('单号', max_length=50, null=False, unique=True)
    # 单号
    date = models.DateField("日期")
    # 日期
    name = models.CharField('名称', max_length=20)
    # 姓名
    money = models.FloatField('金额')
    # 金额
    voucher = models.CharField('凭证', max_length=200)
    # 凭证
    others = models.TextField('备注')
    # 备注
    status = models.IntegerField(default=1)
    # 1 未提交
    # 2 修改中
    # 3 提交未审核
    # 4 申请修改中
    # 5 审核通过
    createTime = models.DateTimeField('创建日期', auto_now_add=True)
    addTime = models.DateTimeField('保存日期', default=timezone.now)
    modifyTime = models.DateTimeField('最后修改日期', auto_now=True)
    # 创建时间
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    # 外键
    show = models.IntegerField(default=1)

class Order(models.Model):
    '''支出的名称、日期、金额、收款人、负责人、凭证
    '''
    id = models.AutoField(primary_key=True)
    # 自增主键
    uuidName = models.CharField('订单编号', max_length=50, null=False, unique=True)
    # 单号
    timeBegin = models.DateField("日期")
    timeExpire = models.DateField("日期")
    # 日期
    course = models.CharField('课程编号', max_length=20)
    # 姓名
    money = models.FloatField('金额')
    # 金额
    voucher = models.CharField('凭证', max_length=200)
    # 凭证
    others = models.TextField('备注')
    # 备注
    status = models.IntegerField(default=1)
    # 1 未提交
    # 2 修改中
    # 3 提交未审核
    # 4 申请修改中
    # 5 审核通过
    createTime = models.DateTimeField('创建日期', auto_now_add=True)
    addTime = models.DateTimeField('保存日期', default=timezone.now)
    modifyTime = models.DateTimeField('最后修改日期', auto_now=True)
    # 创建时间
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # 外键
    show = models.IntegerField(default=1)

