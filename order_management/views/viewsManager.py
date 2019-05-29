from django.shortcuts import render, HttpResponse, redirect
from order_management.models import Manager, Notice
import json
# Create your views here.
# ***************************************************************************
# 用户登录业务逻辑
def login(request):
    method = request.method
    # get请求访问
    if method == 'GET':
        return render(request, 'manager/login.html')
    # post表单请求
    elif method == 'POST':
        post = request.POST
        name = post['name'].strip()
        password = post['password'].strip()
        secret = post['secret'].strip()
        # 是否已经存在
        exist = Manager.objects.filter(name=name)
        # 成功验证
        match = Manager.objects.filter(name=name, password=password, show=1)
        deleted = Manager.objects.filter(name=name, show=0)
        if secret != '35405':
            info = {'error': '公司内部管理员才能访问'}
            return render(request, 'manager/login.html', info)
        # 已经删除
        elif deleted:
            info = {'error': '该用户已被管理员删除'}
            return render(request, 'manager/login.html', info)
        # 登录成功
        elif match:
            # session添加信息
            superManager = match[0].superManager
            session = request.session
            session['name'] = name
            session['superManager'] = superManager
            return redirect('/manage/')
        # 密码错误
        elif exist:
            info = {'error': '密码输入错误'}
            return render(request, 'manager/login.html', info)
        # 用户不存在
        else:
            info = {'error': '用户名不存在'}
            return render(request, 'manager/login.html', info)
            # return redirect('/manage/regist/')

# ***************************************************************************
# 用户注册业务逻辑
def regist(request):
    method = request.method
    # get请求访问
    if method == 'GET':
        return render(request, 'manager/regist.html')
    # post表单请求
    elif method == 'POST':
        post = request.POST
        name = post['name'].strip()
        password = post['password'].strip()
        # 是否已经存在
        exist = Manager.objects.filter(name=name)
        # 名字重复
        if exist:
            info = {'error': '注册姓名已存在，请您&nbsp;<a href="/manage/login/"><input type="button" value="登录"></a>'}
            return render(request, 'manager/regist.html', info)
        else:
            Manager.objects.create(name=name, password=password)
            return redirect('/manage/login/')

# ***************************************************************************
# 用户登录后首页
# 超级管理员0和一般管理员1
def showIndex(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        if superManager == 0:
            managers = Manager.objects.filter(superManager = 1, show=1)
            rawNotices = Notice.objects.filter().values('content')
            notices = [rawNotice['content'] for rawNotice in rawNotices]
            info = {"name": name, 'superManager': superManager,
                'managers': managers, 'notices': notices}
            return render(request, 'manager/index.html', info)
        elif superManager == 1:
            return redirect('/manage/showClients/')

# ***************************************************************************
# 用户注销登录业务逻辑
def vanish(request):
    request.session.clear()
    return redirect('/manage/login/')

# ***************************************************************************
# 用户修改业务逻辑
def changePassword(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        # 请求方式
        method = request.method
        session = request.session
        name = session.get('name', None)
        if method == "GET":
            target = {"name": name}
            return render(request, 'manager/changePassword.html', target)
        elif method == 'POST':
            post = request.POST
            password = post['password']
            Manager.objects.filter(name=name).update(password=password)
            return redirect('/manage/')
        else:
            target = {"name": name, 'error': "输入错误"}
            return render(request, 'manager/changePassword.html', target)


# ***************************************************************************
# 一般用户重置密码业务逻辑
def resetManagerPassword(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 没有权限
    elif superManager != 0:
        return HttpResponse('您没有权限访问')
    # 已经登录
    else:
        if request.method == 'POST':
            post = request.POST
            id = post.get('id')
            Manager.objects.filter(id=id).update(password='88888888')
            target = {'result': True}
            return HttpResponse(json.dumps(target))
        else:
            target = {'result': False}
            return HttpResponse(json.dumps(target))

# ***************************************************************************
# 删除一般用户业务逻辑
def deleteManager(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 没有权限
    elif superManager != 0:
        return HttpResponse('您没有权限访问')
    # 已经登录
    else:
        # post提交
        if request.method == 'POST':
            post = request.POST
            id = post.get('id')
            try:
                Manager.objects.filter(id=id).update(show=0)
            # 修改报错
            except:
                target = {'result': False}
            # 修改正常
            else:
                target = {'result': True}
            finally:
                return HttpResponse(json.dumps(target))
        # 其他提交方式
        else:
            target = {'result': False}
            return HttpResponse(json.dumps(target))

