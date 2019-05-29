from django.shortcuts import render, HttpResponse, redirect
from order_management.models import Manager, Notice, Client, Worker
import json
# Create your views here.
# ***************************************************************************
# 修改公告业务逻辑
def addClient(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        # 获得公告信息
        rawNotices = Notice.objects.filter().values('content')
        notices = [rawNotice['content'] for rawNotice in rawNotices]
        # 请求方式
        method = request.method
        if method == 'GET':
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'client': ""}
            return render(request, 'client/addClient.html', info)
        elif method == 'POST':
            # 获得当前管理员
            managers = Manager.objects.filter(name=name)
            # 创建当前客户
            post = request.POST
            client = Client()
            client.name = post['name'].strip()
            client.realName = post['realName'].strip()
            client.sex = post['sex'].strip()
            client.age = post['age'].strip()
            client.tel = post['tel'].strip()
            client.address = post['address'].strip()
            client.kindergarten = post['kindergarten'].strip()
            client.primarySchool = post['primarySchool'].strip()
            client.junior = post['junior'].strip()
            client.senior = post['senior'].strip()
            client.others = post['others'].strip()
            client.manager = managers[0]
            # 保存成功，姓名唯一
            try:
                client.save()
                # 信息汇总
                return redirect('/manage/showClients')
            # 保存失败，姓名重复，需要更改别名
            except:
                error = '添加失败，姓名已存在。若是新用户，请更改别名继续保存。'
                # 查找所有重名
                multiClients = Client.objects.filter(realName=client.realName)

                info = {"name": name,
                        'superManager': superManager,
                        'notices': notices,
                        'client': client,
                        'multiClients': multiClients,
                        'error': error}
                return render(request, 'client/addClient.html', info)

def showClients(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        # 获得公告信息
        rawNotices = Notice.objects.filter().values('content')
        notices = [rawNotice['content'] for rawNotice in rawNotices]
        method = request.method
        if method == 'GET':
            # 查找所有重名
            multiClients = Client.objects.filter().order_by('status', '-createTime')
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'multiClients': multiClients}
            return render(request, 'client/showClients.html', info)
        elif method == 'POST':
            return HttpResponse('showClients 404')

def searchClients(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        # 获得公告信息
        rawNotices = Notice.objects.filter().values('content')
        notices = [rawNotice['content'] for rawNotice in rawNotices]
        method = request.method
        if method == 'GET':
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices}
            return render(request, 'client/searchClients.html', info)
        elif method == 'POST':
            post = request.POST
            client = Client()
            client.realName = post['realName'].strip()
            client.sex = post['sex'].strip()
            client.age = post['age'].strip()
            client.tel = post['tel'].strip()
            client.address = post['address'].strip()
            client.kindergarten = post['kindergarten'].strip()
            client.primarySchool = post['primarySchool'].strip()
            client.junior = post['junior'].strip()
            client.senior = post['senior'].strip()
            client.others = post['others'].strip()
            targetDict = {}
            for key, value in post.items():
                if value.strip() != '' and key != "csrfmiddlewaretoken":
                    if key == 'sex':
                        targetDict[key] = value
                    else:
                        targetDict[key + "__contains"] = value
            multiClients = Client.objects.filter(**targetDict).order_by('status', '-createTime')
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'client': client,
                    'multiClients': multiClients}
            return render(request, 'client/searchClients.html', info)

def getClients(request):
    session = request.session
    name = session.get('name', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        # post提交
        if request.method == 'POST':
            post = request.POST
            # 初始化
            targetDict = {}
            for key, value in post.items():
                if value.strip() != '' and key != "csrfmiddlewaretoken":
                    if key == 'sex':
                        targetDict[key] = value
                    else:
                        targetDict[key + "__contains"] = value
            multiClients = Client.objects.filter(**targetDict).order_by('status', '-createTime')
            if len(multiClients) >= 6:
                multiClients = multiClients[0:5]
            clients = [[client.id, client.realName, client.sex, client.kindergarten, client.primarySchool,
                        client.junior, client.senior, client.address] for client in multiClients]
            target = {'result': True, 'multiClients': clients}
            return HttpResponse(json.dumps(target))
        # 其他提交方式
        else:
            target = {'result': False}
            return HttpResponse(json.dumps(target))

def modifyClient(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        # 获得公告信息
        rawNotices = Notice.objects.filter().values('content')
        notices = [rawNotice['content'] for rawNotice in rawNotices]
        # 请求方式
        method = request.method
        if method == 'GET':
            get = request.GET
            id = get['id']
            clients = Client.objects.filter(id__exact=id)
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'client': ""}
            if len(clients) == 1:
                request.session['clientId'] = id
                client = clients[0]
                # 请求验证##############################################1、2
                if client.status == 1 or client.status == 2:
                    info['client'] = client
                    return render(request, 'client/modifyClient.html', info)
                else:
                    return HttpResponse('No right to modify Client')
            else:
                return HttpResponse('modifyClient 404')
        elif method == 'POST':
            clientId = request.session['clientId']
            del request.session['clientId']
            # 获得当前管理员
            managers = Manager.objects.filter(name=name)
            # 创建当前客户
            post = request.POST

            # 不可更改？？？？？？？？？？？
            uname = post['name'].strip()

            age = post['age'].strip()
            # 不可更改？？？？？？？？？？？

            # 验证
            clients = Client.objects.filter(id__exact=clientId)
            # 报错，必须唯一
            if len(clients) != 1:
                return HttpResponse('No right to modify Client')
            else:
                client = clients[0]
                # 请求验证##############################################1、2
                if client.status != 1 and client.status != 2:
                    return HttpResponse('No right to modify Client')
                else:
                    realName = post['realName'].strip()
                    sex = post['sex'].strip()
                    tel = post['tel'].strip()
                    address = post['address'].strip()
                    kindergarten = post['kindergarten'].strip()
                    primarySchool = post['primarySchool'].strip()
                    junior = post['junior'].strip()
                    senior = post['senior'].strip()
                    others = post['others'].strip()
                    manager = managers[0]
                    Client.objects.filter(id=clientId).update(realName=realName, sex=sex, tel=tel, address=address, kindergarten=kindergarten, primarySchool=primarySchool, junior=junior, senior=senior, others=others, manager=manager)
                    return redirect('/manage/showClients/')
        else:
            return HttpResponse('modifyClient 404')

def deleteClient(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        # post提交
        if request.method == 'POST':
            post = request.POST
            id = post.get('id')
            # 状态验证
            clients = Client.objects.filter(id=id)
            # 报错不唯一
            if len(clients) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                client = clients[0]
                # 不是可删除状态
                if client.status != 1:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Client.objects.filter(id=id).delete()
                    # 删除报错
                    except:
                        target = {'result': False}
                    # 删除正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
        # 其他提交方式
        else:
            target = {'result': False}
            return HttpResponse(json.dumps(target))

def submitClient(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        # post提交
        if request.method == 'POST':
            post = request.POST
            id = post.get('id')
            # 状态验证
            clients = Client.objects.filter(id=id)
            # 报错不唯一
            if len(clients) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                client = clients[0]
                # 不是可提交状态
                if client.status != 1 and client.status != 2:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Client.objects.filter(id=id).update(status=3)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
        # 其他提交方式
        else:
            target = {'result': False}
            return HttpResponse(json.dumps(target))

def applyClient(request):
    session = request.session
    name = session.get('name', None)
    superManager = session.get('superManager', None)
    # 还没登录
    if name == None:
        return redirect('/manage/login/')
    # 已经登录
    else:
        # post提交
        if request.method == 'POST':
            post = request.POST
            id = post.get('id')
            # 状态验证
            clients = Client.objects.filter(id=id)
            # 报错不唯一
            if len(clients) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                client = clients[0]
                # 不是可提交状态
                if client.status != 5:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Client.objects.filter(id=id).update(status=4)
                    # 申请修改报错
                    except:
                        target = {'result': False}
                    # 申请修改正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
        # 其他提交方式
        else:
            target = {'result': False}
            return HttpResponse(json.dumps(target))

def passClient(request):
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
            # 状态验证
            clients = Client.objects.filter(id=id)
            # 报错: 不唯一
            if len(clients) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                client = clients[0]
                # 提交未审核
                if client.status == 3:
                    try:
                        Client.objects.filter(id=id).update(status=5)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                # 申请修改
                elif client.status == 4:
                    try:
                        Client.objects.filter(id=id).update(status=2)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                else:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
        # 其他提交方式
        else:
            target = {'result': False}
            return HttpResponse(json.dumps(target))

def unPassClient(request):
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
            # 状态验证
            clients = Client.objects.filter(id=id)
            # 报错: 不唯一
            if len(clients) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                client = clients[0]
                # 提交未审核
                if client.status == 3:
                    try:
                        Client.objects.filter(id=id).update(status=1)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                # 申请修改
                elif client.status == 4:
                    try:
                        Client.objects.filter(id=id).update(status=5)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                else:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
        # 其他提交方式
        else:
            target = {'result': False}
            return HttpResponse(json.dumps(target))
