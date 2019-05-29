from django.shortcuts import render, HttpResponse, redirect
from order_management.models import Manager, Notice
import json
# Create your views here.
# ***************************************************************************
# 修改公告业务逻辑
def modifyNotice(request):
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
        method = request.method
        if method == 'GET':
            rawNotices = Notice.objects.filter().values('content')
            notices = [rawNotice['content'] for rawNotice in rawNotices]
            info = {"name": name, 'superManager': superManager, 'notices': notices}
            return render(request, 'notice/changeNotice.html', info)
        elif method == 'POST':
            # 全部清空
            Notice.objects.filter().delete()
            # 获得传值
            post = request.POST
            for key, value in post.items():
                if key != "csrfmiddlewaretoken":
                    # 去空格
                    value = value.strip()
                    # 非空公告
                    if value != "":
                        Notice.objects.create(content=value)
            # 全部查出
            rawNotices = Notice.objects.filter().values('content')
            notices = [rawNotice['content'] for rawNotice in rawNotices]
            info = {"name": name, 'superManager': superManager, 'notices': notices}
            return render(request, 'notice/changeNotice.html', info)