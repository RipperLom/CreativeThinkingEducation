from django.shortcuts import render, HttpResponse, redirect
from order_management.models import Manager, Notice, Client, Worker, Expense
import json, uuid, datetime, os, re
from django.conf import settings

# Create your views here.
# ***************************************************************************
def addExpense(request):
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
                    'expense': ""}
            return render(request, 'expense/addExpense.html', info)
        elif method == 'POST':

            # 创建当前客户
            post = request.POST
            expense = Expense()
            # uuid
            expense.uuidName = uuid.uuid1()
            # 名称
            expense.name = post['name'].strip()
            # 日期
            expense.date = post['date'].strip()
            # 金额
            expense.money = post['money'].strip()
            # 备注
            expense.others = post['others'].strip()
            # 管理员
            managers = Manager.objects.filter(name=name)
            expense.manager = managers[0]
        # ==============================================================================
        # 收款人验证
            try:
                workerId = post['workerId'].strip()
                expense.worker = Worker.objects.filter(id=workerId)[0]
            except:
                error = '添加失败，请选择收款人。'
                info = {"name": name,
                        'superManager': superManager,
                        'notices': notices,
                        'expense': expense,
                        'error': error}
                return render(request, 'expense/addExpense.html', info)
        # ==============================================================================
        # ==============================================================================
        # 照片凭证
            files = request.FILES
            image = files.get('voucherPicture', None)
            if image == None:# 没有上传凭证
                # 保存
                try:
                    expense.save()
                    return redirect('/manage/showExpenses')
                # 保存失败，姓名重复，需要更改别名
                except:
                    error = '添加失败，请重试。'
                    info = {"name": name,
                            'superManager': superManager,
                            'notices': notices,
                            'expense': expense,
                            'error': error}
                    return render(request, 'expense/addExpense.html', info)
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
                            'expense': expense,
                            'error': error}
                    return render(request, 'expense/addExpense.html', info)
            # ==============================================================================

                # 照片名字
                fileName = str(datetime.datetime.today()) + "_" + str(expense.uuidName)
                split = re.split(" |-|:|\.", fileName)
                fileName = "_".join(split) + "." + fileType
                # 父路径
                fatherURL = settings.STATICFILES_DIRS[0]
                fatherURL = os.path.join(fatherURL, 'img')
                fatherURL = os.path.join(fatherURL, 'manage')
                fatherURL = os.path.join(fatherURL, 'cost')
                fatherURL = os.path.join(fatherURL, 'voucher')
                # 文件路径
                fileURL = os.path.join(fatherURL, fileName)
                expense.voucher = '/static/img/manage/cost/voucher/' + fileName
            # ==============================================================================
            # 验证照片类型通过，保存数据和文件
                try:# 保存
                    expense.save()
                    # 保存成功后，存储文件
                    with open(fileURL, 'wb') as f:
                        for line in image.chunks():
                            f.write(line)
                    # 信息汇总
                    return redirect('/manage/showExpenses')
                # 保存失败，姓名重复，需要更改别名
                except:
                    error = '添加失败，请重试。'
                    info = {"name": name,
                            'superManager': superManager,
                            'notices': notices,
                            'expense': expense,
                            'error': error}
                    return render(request, 'expense/addExpense.html', info)


def showExpenses(request):
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
            multiExpenses = Expense.objects.filter().order_by('status', '-createTime')
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'multiExpenses': multiExpenses}
            return render(request, 'expense/showExpenses.html', info)
        elif method == 'POST':
            return HttpResponse('showExpenses 404')


def searchExpenses(request):
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
            return render(request, 'expense/searchExpenses.html', info)
        elif method == 'POST':
            targetDict = {}
            # 创建当前客户
            post = request.POST
            expense = Expense()
            worker = Worker()
            worker.realName = post['workerRealName'].strip()
            worker.sex = post['workerSex'].strip()
            worker.subject = post['workerSubject'].strip()
            worker.tel = post['workerTel'].strip()
            # 名称
            expense.name = post['name'].strip()
            targetDict['name' + "__contains"] = expense.name
            # 日期
            dateBegin = post['dateBegin'].strip()
            if dateBegin != '':
                targetDict['date__gte'] = dateBegin
            dateExpire = post['dateExpire'].strip()
            if dateExpire != '':
                targetDict['date__lte'] = dateExpire
            # 金额
            expense.money = post['money'].strip()
            if expense.money != '':
                targetDict['money'] = expense.money
            # 备注
            expense.others = post['others'].strip()
            targetDict['others' + "__contains"] = expense.others
            # 回显信息
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'expense': expense,
                    'dateBegin': dateBegin,
                    'dateExpire': dateExpire}
            try:
                workerId = post['workerId'].strip()
            except:
                info['worker'] = worker
            else:
                targetDict['worker__id'] = workerId
                expense.worker = Worker.objects.filter(id=workerId)[0]
                info['worker'] = expense.worker
            finally:
                multiExpenses = Expense.objects.filter(**targetDict).order_by('status', '-createTime')
                info['multiExpenses'] = multiExpenses
                return render(request, 'expense/searchExpenses.html', info)


def modifyExpense(request):
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
            expenses = Expense.objects.filter(id__exact=id)
            info = {"name": name,
                    'superManager': superManager,
                    'notices': notices,
                    'expense': ""}
            if len(expenses) == 1:
                request.session['expenseId'] = id
                expense = expenses[0]
                # 请求验证##############################################1、2
                if expense.status == 1 or expense.status == 2:
                    info['expense'] = expense
                    info['worker'] = expense.worker
                    return render(request, 'expense/modifyExpense.html', info)
                else:
                    return HttpResponse('No right to modify Expense')
            else:
                return HttpResponse('modifyExpense 404')
        elif method == 'POST':
            expenseId = request.session['expenseId']
            del request.session['expenseId']

            # 验证唯一性
            expenses = Expense.objects.filter(id__exact=expenseId)
            # 报错，必须唯一
            if len(expenses) != 1:
                return HttpResponse('No right to modify Expense')
            else:
                expense = expenses[0]
                # 请求验证##############################################1、2
                if expense.status != 1 and expense.status != 2:
                    return HttpResponse('No right to modify Expense')
                else:
                    # 创建当前客户
                    post = request.POST
                    # 名称
                    expense.name = post['name'].strip()
                    # 日期
                    expense.date = post['date'].strip()
                    # 金额
                    expense.money = post['money'].strip()
                    # 备注
                    expense.others = post['others'].strip()
                    # 管理员
                    managers = Manager.objects.filter(name=name)
                    expense.manager = managers[0]

                    # 收款人验证
                    try:
                        workerId = post['workerId'].strip()
                        expense.worker = Worker.objects.filter(id=workerId)[0]
                    except:
                        expense.worker = Expense.objects.filter(id=expenseId)[0].worker
                    finally:
                        files = request.FILES
                        image = files.get('voucherPicture', None)
                        if image == None:  # 没有上传凭证
                            try:
                                Expense.objects.filter(id=expenseId).update(name=expense.name, date=expense.date,
                                                                            money=expense.money, others=expense.others,
                                                                            worker=expense.worker,
                                                                            manager=expense.manager)
                                # 信息汇总
                                return redirect('/manage/showExpenses')

                            except:
                                error = '添加失败，请重试。'
                                info = {"name": name,
                                        'superManager': superManager,
                                        'notices': notices,
                                        'expense': expense,
                                        'worker': expense.worker,
                                        'error': error}
                                return render(request, 'expense/modifyExpense.html', info)
                        else:   # 上传凭证
                        # ==============================================================================
                        # 验证照片类型
                            fileType = image.name.split('.')[-1]
                            if fileType == 'bmp' or fileType == 'jpg' or fileType == 'jpeg' or fileType == 'png' or fileType == 'pdf':
                                pass
                            else:
                                request.session['expenseId'] = expenseId
                                error = '请添加照片格式文件。'
                                info = {"name": name,
                                        'superManager': superManager,
                                        'notices': notices,
                                        'expense': expense,
                                        'worker': expense.worker,
                                        'error': error}
                                return render(request, 'expense/modifyExpense.html', info)
                        # ==============================================================================
                            # 照片名字
                            fileName = str(datetime.datetime.today()) + "_" + str(expense.uuidName)
                            split = re.split(" |-|:|\.", fileName)
                            fileName = "_".join(split) + "." + fileType
                            # 父路径
                            fatherURL = settings.STATICFILES_DIRS[0]
                            fatherURL = os.path.join(fatherURL, 'img')
                            fatherURL = os.path.join(fatherURL, 'manage')
                            fatherURL = os.path.join(fatherURL, 'cost')
                            fatherURL = os.path.join(fatherURL, 'voucher')
                            # 文件路径
                            fileURL = os.path.join(fatherURL, fileName)
                            expense.voucher = '/static/img/manage/cost/voucher/' + fileName
                            try:
                                Expense.objects.filter(id=expenseId).update(name=expense.name, date=expense.date,
                                                                        money=expense.money, others=expense.others,
                                                                        worker=expense.worker, manager=expense.manager,
                                                                        voucher=expense.voucher)
                                # 存储文件
                                with open(fileURL, 'wb') as f:
                                    for line in image.chunks():
                                        f.write(line)
                                # 信息汇总
                                return redirect('/manage/showExpenses')

                            except:
                                error = '添加失败，请重试。'
                                info = {"name": name,
                                        'superManager': superManager,
                                        'notices': notices,
                                        'expense': expense,
                                        'worker': expense.worker,
                                        'error': error}
                                return render(request, 'expense/modifyExpense.html', info)


        else:
            return HttpResponse('modifyExpense 404')


def deleteExpense(request):
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
            expenses = Expense.objects.filter(id=id)
            # 报错不唯一
            if len(expenses) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                expense = expenses[0]
                # 不是可删除状态
                if expense.status != 1:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Expense.objects.filter(id=id).delete()
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


def submitExpense(request):
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
            expenses = Expense.objects.filter(id=id)
            # 报错不唯一
            if len(expenses) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                expense = expenses[0]
                # 不是可提交状态
                if expense.status != 1 and expense.status != 2:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Expense.objects.filter(id=id).update(status=3)
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


def applyExpense(request):
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
            expenses = Expense.objects.filter(id=id)
            # 报错不唯一
            if len(expenses) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                expense = expenses[0]
                # 不是可提交状态
                if expense.status != 5:
                    target = {'result': False}
                    return HttpResponse(json.dumps(target))
                else:
                    try:
                        Expense.objects.filter(id=id).update(status=4)
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


def passExpense(request):
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
            expenses = Expense.objects.filter(id=id)
            # 报错: 不唯一
            if len(expenses) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                expense = expenses[0]
                # 提交未审核
                if expense.status == 3:
                    try:
                        Expense.objects.filter(id=id).update(status=5)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                # 申请修改
                elif expense.status == 4:
                    try:
                        Expense.objects.filter(id=id).update(status=2)
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


def unPassExpense(request):
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
            expenses = Expense.objects.filter(id=id)
            # 报错: 不唯一
            if len(expenses) != 1:
                target = {'result': False}
                return HttpResponse(json.dumps(target))
            else:
                expense = expenses[0]
                # 提交未审核
                if expense.status == 3:
                    try:
                        Expense.objects.filter(id=id).update(status=1)
                    # 提交报错
                    except:
                        target = {'result': False}
                    # 提交正常
                    else:
                        target = {'result': True}
                    finally:
                        return HttpResponse(json.dumps(target))
                # 申请修改
                elif expense.status == 4:
                    try:
                        Expense.objects.filter(id=id).update(status=5)
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

