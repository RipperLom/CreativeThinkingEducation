from django.shortcuts import render, HttpResponse, redirect
from order_management.models import Manager, Notice, Client, Worker, Expense, Order
import json, uuid, datetime, os, re
from django.conf import settings

# Create your views here.
# ***************************************************************************
def addOrder(request):
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
                    'order': ""}
            return render(request, 'order/addOrder.html', info)
        elif method == 'POST':

            # 创建当前客户
            post = request.POST
            order = Order()
            # uuid
            order.uuidName = uuid.uuid1()
            # 名称
            order.course = post['course'].strip()
            # 日期
            order.timeBegin = post['timeBegin'].strip()
            order.timeExpire = post['timeExpire'].strip()
            # 金额
            order.money = post['money'].strip()
            # 备注
            order.others = post['others'].strip()
            # 管理员
            managers = Manager.objects.filter(name=name)
            order.manager = managers[0]
        # ==============================================================================
        # 收款人验证
            try:
                workerId = post['workerId'].strip()
                order.worker = Worker.objects.filter(id=workerId)[0]
                clientId = post['clientId'].strip()
                order.client = Client.objects.filter(id=clientId)[0]
            except:
                error = '添加失败，请选择员工和学生。'
                info = {"name": name,
                        'superManager': superManager,
                        'notices': notices,
                        'order': order,
                        'error': error}
                return render(request, 'order/addOrder.html', info)
        # ==============================================================================
        # ==============================================================================
        # 照片凭证
            files = request.FILES
            image = files.get('voucherPicture', None)
            if image == None:# 没有上传凭证
                # 保存
                try:
                    order.save()
                    return redirect('/manage/showOrders')
                # 保存失败，姓名重复，需要更改别名
                except:
                    error = '添加失败，请重试。'
                    info = {"name": name,
                            'superManager': superManager,
                            'notices': notices,
                            'order': order,
                            'error': error}
                    return render(request, 'order/addOrder.html', info)
        # ==============================================================================
            else:# 上传凭证
            # ==============================================================================
            # 验证照片类型
                fileType = image.name.split('.')[-1]
                if fileType == 'bmp' or fileType == 'jpg' or fileType == 'jpeg' or fileType == 'png' or fileType == 'pdf':
                    pass
                else:
                    error = '请添加照片格式。'
                    info = {"name": name,
                            'superManager': superManager,
                            'notices': notices,
                            'order': order,
                            'error': error}
                    return render(request, 'order/addOrder.html', info)
            # ==============================================================================

                # 照片名字
                fileName = str(datetime.datetime.today()) + "_" + str(order.uuidName)
                split = re.split(" |-|:|\.", fileName)
                fileName = "_".join(split) + "." + fileType
                # 父路径
                fatherURL = settings.STATICFILES_DIRS[0]
                fatherURL = os.path.join(fatherURL, 'img')
                fatherURL = os.path.join(fatherURL, 'manage')
                fatherURL = os.path.join(fatherURL, 'order')
                fatherURL = os.path.join(fatherURL, 'voucher')
                # 文件路径
                fileURL = os.path.join(fatherURL, fileName)
                order.voucher = '/static/img/manage/order/voucher/' + fileName
            # ==============================================================================
            # 验证照片类型通过，保存数据和文件
                try:# 保存
                    order.save()
                    # 保存成功后，存储文件
                    with open(fileURL, 'wb') as f:
                        for line in image.chunks():
                            f.write(line)
                    # 信息汇总
                    return redirect('/manage/showOrders')
                # 保存失败，姓名重复，需要更改别名
                except:
                    error = '添加失败，请重试。'
                    info = {"name": name,
                            'superManager': superManager,
                            'notices': notices,
                            'order': order,
                            'error': error}
                    return render(request, 'order/addOrder.html', info)


def showOrders(request):
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
            multiOrders = Order.objects.filter().order_by('status', '-createTime')
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'multiOrders': multiOrders}
            return render(request, 'order/showOrders.html', info)
        elif method == 'POST':
            return HttpResponse('showOrders 404')


def searchOrders(request):
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
            return render(request, 'order/searchOrders.html', info)
        elif method == 'POST':
            targetDict = {}
            # 创建当前客户
            post = request.POST
            order = Order()
            client = Client()
            worker = Worker()
            client.realName = post['clientRealName'].strip()
            client.sex = post['clientSex'].strip()
            client.kindergarten = post['clientKindergarten'].strip()
            client.primarySchool = post['clientPrimarySchool'].strip()
            client.junior = post['clientJunior'].strip()
            client.senior = post['clientSenior'].strip()
            client.address = post['clientAddress'].strip()

            worker.realName = post['workerRealName'].strip()
            worker.sex = post['workerSex'].strip()
            worker.subject = post['workerSubject'].strip()
            worker.tel = post['workerTel'].strip()
            # 名称
            order.course = post['course'].strip()
            targetDict['course' + "__contains"] = order.course
            # 日期
            dateBegin = post['dateBegin'].strip()
            if dateBegin != '':
                targetDict['timeExpire__gte'] = dateBegin
            dateExpire = post['dateExpire'].strip()
            if dateExpire != '':
                targetDict['timeBegin__lte'] = dateExpire
            # 金额
            order.money = post['money'].strip()
            if order.money != '':
                targetDict['money'] = order.money
            # 备注
            order.others = post['others'].strip()
            targetDict['others' + "__contains"] = order.others
            # 回显信息
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'order': order,
                    'dateBegin': dateBegin,
                    'dateExpire': dateExpire}
            try:
                workerId = post['workerId'].strip()

            except:
                info['worker'] = worker

            else:
                targetDict['worker__id'] = workerId
                order.worker = Worker.objects.filter(id=workerId)[0]
                info['worker'] = order.worker

            try:

                clientId = post['clientId'].strip()
            except:

                info['client'] = client
            else:

                targetDict['client__id'] = clientId
                order.client = Client.objects.filter(id=clientId)[0]
                info['client'] = order.client

            multiOrders = Order.objects.filter(**targetDict).order_by('status', '-createTime')
            info['multiOrders'] = multiOrders
            return render(request, 'order/searchOrders.html', info)


def modifyOrder(request):
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
            orders = Order.objects.filter(id__exact=id)
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'order': ""}
            if len(orders) == 1:
                request.session['orderId'] = id
                order = orders[0]
                # 请求验证##############################################1、2
                if order.status == 1 or order.status == 2:
                    info['order'] = order
                    info['worker'] = order.worker
                    info['client'] = order.client
                    return render(request, 'order/modifyOrder.html', info)
                else:
                    return HttpResponse('No right to modify Order')
            else:
                return HttpResponse('modifyOrder 404')
        elif method == 'POST':
            orderId = request.session['orderId']
            del request.session['orderId']
            # 验证唯一性
            orders = Order.objects.filter(id__exact=orderId)
            # 报错，必须唯一
            if len(orders) != 1:
                return HttpResponse('No right to modify Order')
            else:
                order = orders[0]
                # 请求验证##############################################1、2
                if order.status != 1 and order.status != 2:
                    return HttpResponse('No right to modify Order')
                else:
                    # 创建当前客户
                    post = request.POST
                    order = Order()
                    # 名称
                    order.course = post['course'].strip()
                    # 日期
                    order.timeBegin = post['timeBegin'].strip()
                    order.timeExpire = post['timeExpire'].strip()
                    # 金额
                    order.money = post['money'].strip()
                    # 备注
                    order.others = post['others'].strip()
                    # 管理员
                    managers = Manager.objects.filter(name=name)
                    order.manager = managers[0]

                    # 收款人验证
                    try:
                        workerId = post['workerId'].strip()
                        order.worker = Worker.objects.filter(id=workerId)[0]
                        clientId = post['clientId'].strip()
                        order.client = Client.objects.filter(id=clientId)[0]
                    except:
                        order.worker = Order.objects.filter(id=orderId)[0].worker
                        order.client = Order.objects.filter(id=orderId)[0].client
                    finally:
                        files = request.FILES
                        image = files.get('voucherPicture', None)
                        print(image)
                        if image == None:  # 没有上传凭证
                            try:
                                Order.objects.filter(id=orderId).update(course=order.course, timeBegin=order.timeBegin,
                                                                        timeExpire=order.timeExpire,
                                                                            money=order.money, others=order.others,
                                                                            worker=order.worker, client=order.client,
                                                                            manager=order.manager)
                                # 信息汇总
                                return redirect('/manage/showOrders')

                            except:
                                error = '添加失败，请重试。'
                                info = {"name": name,
                                        'superManager': superManager,
                                        'notices': notices,
                                        'order': order,
                                        'worker': order.worker,
                                        'client': order.client,
                                        'error': error}
                                return render(request, 'order/modifyOrder.html', info)
                        else:   # 上传凭证
                        # ==============================================================================
                        # 验证照片类型
                            fileType = image.name.split('.')[-1]
                            if fileType == 'bmp' or fileType == 'jpg' or fileType == 'jpeg' or fileType == 'png' or fileType == 'pdf':
                                pass
                            else:
                                request.session['orderId'] = orderId
                                error = '请添加照片格式文件。'
                                info = {"name": name,
                                        'superManager': superManager,
                                        'notices': notices,
                                        'order': order,
                                        'worker': order.worker,
                                        'client': order.client,
                                        'error': error}
                                return render(request, 'order/modifyOrder.html', info)
                        # ==============================================================================
                            # 照片名字
                            fileName = str(datetime.datetime.today()) + "_" + str(order.uuidName)
                            split = re.split(" |-|:|\.", fileName)
                            fileName = "_".join(split) + "." + fileType
                            # 父路径
                            fatherURL = settings.STATICFILES_DIRS[0]
                            fatherURL = os.path.join(fatherURL, 'img')
                            fatherURL = os.path.join(fatherURL, 'manage')
                            fatherURL = os.path.join(fatherURL, 'order')
                            fatherURL = os.path.join(fatherURL, 'voucher')
                            # 文件路径
                            fileURL = os.path.join(fatherURL, fileName)
                            order.voucher = '/static/img/manage/order/voucher/' + fileName
                            try:
                                Order.objects.filter(id=orderId).update(course=order.course, timeBegin=order.timeBegin,
                                                                        timeExpire=order.timeExpire,
                                                                        money=order.money, others=order.others,
                                                                        worker=order.worker, client=order.client,
                                                                        manager=order.manager,
                                                                        voucher=order.voucher)
                                # 存储文件
                                with open(fileURL, 'wb') as f:
                                    for line in image.chunks():
                                        f.write(line)
                                # 信息汇总
                                return redirect('/manage/showOrders')

                            except:
                                error = '添加失败，请重试。'
                                info = {"name": name,
                                        'superManager': superManager,
                                        'notices': notices,
                                        'order': order,
                                        'worker': order.worker,
                                        'client': order.client,
                                        'error': error}
                                return render(request, 'order/modifyOrder.html', info)


        else:
            return HttpResponse('modifyOrder 404')


def deleteOrder(request):
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
            orders = Order.objects.filter(id=id)
            # 报错不唯一
            if len(orders) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                order = orders[0]
                # 不是可删除状态
                if order.status != 1:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Order.objects.filter(id=id).delete()
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


def submitOrder(request):
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
            orders = Order.objects.filter(id=id)
            # 报错不唯一
            if len(orders) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                order = orders[0]
                # 不是可提交状态
                if order.status != 1 and order.status != 2:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Order.objects.filter(id=id).update(status=3)
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


def applyOrder(request):
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
            orders = Order.objects.filter(id=id)
            # 报错不唯一
            if len(orders) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                order = orders[0]
                # 不是可提交状态
                if order.status != 5:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Order.objects.filter(id=id).update(status=4)
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


def passOrder(request):
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
            orders = Order.objects.filter(id=id)
            # 报错: 不唯一
            if len(orders) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                order = orders[0]
                # 提交未审核
                if order.status == 3:
                    try:
                        Order.objects.filter(id=id).update(status=5)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                # 申请修改
                elif order.status == 4:
                    try:
                        Order.objects.filter(id=id).update(status=2)
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


def unPassOrder(request):
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
            orders = Order.objects.filter(id=id)
            # 报错: 不唯一
            if len(orders) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                order = orders[0]
                # 提交未审核
                if order.status == 3:
                    try:
                        Order.objects.filter(id=id).update(status=1)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                # 申请修改
                elif order.status == 4:
                    try:
                        Order.objects.filter(id=id).update(status=5)
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
