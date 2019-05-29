from django.shortcuts import render, HttpResponse, redirect
from order_management.models import Manager, Notice, Client, Worker, Expense
import json


# Create your views here.
# ***************************************************************************
# 修改公告业务逻辑
def addWorker(request):
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
                    'worker': ""}
            return render(request, 'worker/addWorker.html', info)
        elif method == 'POST':
            # 获得当前管理员
            managers = Manager.objects.filter(name=name)
            # 创建当前客户
            post = request.POST
            worker = Worker()
            worker.name = post['name'].strip()
            worker.realName = post['realName'].strip()
            worker.sex = post['sex'].strip()
            worker.tel = post['tel'].strip()
            worker.subject = post['subject'].strip()

            worker.others = post['others'].strip()
            worker.manager = managers[0]
            # 保存成功，姓名唯一
            try:
                worker.save()
                # 信息汇总
                return redirect('/manage/showWorkers')
            # 保存失败，姓名重复，需要更改别名
            except:
                error = '添加失败，姓名已存在。若是新用户，请更改别名继续保存。'
                # 查找所有重名
                multiWorkers = Worker.objects.filter(realName=worker.realName)

                info = {"name": name,
                        'superManager': superManager,
                        'notices': notices,
                        'worker': worker,
                        'multiWorkers': multiWorkers,
                        'error': error}
                return render(request, 'worker/addWorker.html', info)


def showWorkers(request):
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
            multiWorkers = Worker.objects.filter().order_by('status', '-createTime')
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'multiWorkers': multiWorkers}
            return render(request, 'worker/showWorkers.html', info)
        elif method == 'POST':
            return HttpResponse('showWorkers 404')


def searchWorkers(request):
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
            return render(request, 'worker/searchWorkers.html', info)
        elif method == 'POST':
            post = request.POST
            worker = Worker()
            worker.name = post['name'].strip()
            worker.realName = post['realName'].strip()
            worker.sex = post['sex'].strip()
            worker.tel = post['tel'].strip()
            worker.subject = post['subject'].strip()
            worker.others = post['others'].strip()
            targetDict = {}
            for key, value in post.items():
                if value.strip() != '' and key != "csrfmiddlewaretoken":
                    if key == 'sex':
                        targetDict[key] = value
                    else:
                        targetDict[key + "__contains"] = value
            multiWorkers = Worker.objects.filter(**targetDict).order_by('status', '-createTime')
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'worker': worker,
                    'multiWorkers': multiWorkers}
            return render(request, 'worker/searchWorkers.html', info)


def getWorkers(request):
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
            multiWorkers = Worker.objects.filter(**targetDict).order_by('status', '-createTime')
            if len(multiWorkers) >= 6:
                multiWorkers = multiWorkers[0:5]
            workers = [[worker.id, worker.realName, worker.sex, worker.subject, worker.tel] for worker in multiWorkers]

            target = {'result': True, 'multiWorkers': workers}
            return HttpResponse(json.dumps(target))
        # 其他提交方式
        else:
            target = {'result': False}
            return HttpResponse(json.dumps(target))



def modifyWorker(request):
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
            workers = Worker.objects.filter(id__exact=id)
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'worker': ""}
            if len(workers) == 1:
                request.session['workerId'] = id
                worker = workers[0]
                # 请求验证##############################################1、2
                if worker.status == 1 or worker.status == 2:
                    info['worker'] = worker
                    return render(request, 'worker/modifyWorker.html', info)
                else:
                    return HttpResponse('No right to modify Worker')
            else:
                return HttpResponse('modifyWorker 404')
        elif method == 'POST':
            workerId = request.session['workerId']
            del request.session['workerId']
            # 获得当前管理员
            managers = Manager.objects.filter(name=name)
            # 创建当前客户
            post = request.POST

            # 不可更改？？？？？？？？？？？
            uname = post['name'].strip()
            # 不可更改？？？？？？？？？？？

            # 验证
            workers = Worker.objects.filter(id__exact=workerId)
            # 报错，必须唯一
            if len(workers) != 1:
                return HttpResponse('No right to modify Worker')
            else:
                worker = workers[0]
                # 请求验证##############################################1、2
                if worker.status != 1 and worker.status != 2:
                    return HttpResponse('No right to modify Worker')
                else:

                    realName = post['realName'].strip()
                    sex = post['sex'].strip()
                    tel = post['tel'].strip()
                    others = post['others'].strip()
                    subject = post['subject'].strip()
                    manager = managers[0]
                    Worker.objects.filter(id=workerId).update(realName=realName, sex=sex, tel=tel, others=others,
                                                              manager=manager, subject=subject)
                    return redirect('/manage/showWorkers/')
        else:
            return HttpResponse('modifyWorker 404')


def deleteWorker(request):
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
            id = post.get('id')
            # 状态验证
            workers = Worker.objects.filter(id=id)
            # 报错不唯一
            if len(workers) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                worker = workers[0]
                # 不是可删除状态
                if worker.status != 1:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Worker.objects.filter(id=id).delete()
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


def submitWorker(request):
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
            workers = Worker.objects.filter(id=id)
            # 报错不唯一
            if len(workers) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                worker = workers[0]
                # 不是可提交状态
                if worker.status != 1 and worker.status != 2:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Worker.objects.filter(id=id).update(status=3)
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


def applyWorker(request):
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
            workers = Worker.objects.filter(id=id)
            # 报错不唯一
            if len(workers) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                worker = workers[0]
                # 不是可提交状态
                if worker.status != 5:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Worker.objects.filter(id=id).update(status=4)
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


def passWorker(request):
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
            workers = Worker.objects.filter(id=id)
            # 报错: 不唯一
            if len(workers) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                worker = workers[0]
                # 提交未审核
                if worker.status == 3:
                    try:
                        Worker.objects.filter(id=id).update(status=5)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                # 申请修改
                elif worker.status == 4:
                    try:
                        Worker.objects.filter(id=id).update(status=2)
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


def unPassWorker(request):
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
            workers = Worker.objects.filter(id=id)
            # 报错: 不唯一
            if len(workers) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                worker = workers[0]
                # 提交未审核
                if worker.status == 3:
                    try:
                        Worker.objects.filter(id=id).update(status=1)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                # 申请修改
                elif worker.status == 4:
                    try:
                        Worker.objects.filter(id=id).update(status=5)
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


