"""CreativeThinkingEducation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from order_management.views.viewsManager import login, regist, showIndex, vanish, \
    resetManagerPassword, deleteManager, changePassword
from order_management.views.viewsNotice import modifyNotice
from order_management.views.viewsClient import addClient, showClients, \
    modifyClient, deleteClient, submitClient, passClient, unPassClient, applyClient, searchClients, getClients
from order_management.views.viewsWorker import addWorker, showWorkers, \
modifyWorker, deleteWorker, submitWorker, passWorker, unPassWorker, applyWorker, searchWorkers, getWorkers
from order_management.views.viewsExpense import addExpense, showExpenses, \
modifyExpense, deleteExpense, submitExpense, passExpense, unPassExpense, applyExpense, searchExpenses
from order_management.views.viewsOrder import addOrder, showOrders, \
modifyOrder, deleteOrder, submitOrder, passOrder, unPassOrder, applyOrder, searchOrders



urlpatterns = [
    # Manager***************************************************
    # 登录注册注销改密
    path('login/', login),
    path('regist/', regist),
    path('changePassword/', changePassword),
    path('vanish/', vanish),
    # 管理一般用户
    path('resetManagerPassword/', resetManagerPassword),
    path('deleteManager/', deleteManager),

    # Notice***************************************************
    # 管理公告
    path('modifyNotice/', modifyNotice),

    # Client***************************************************
    # 管理客户
    path('addClient/', addClient),
    path('showClients/', showClients),
    path('modifyClient/', modifyClient),
    path('deleteClient/', deleteClient),
    path('submitClient/', submitClient),
    path('passClient/', passClient),
    path('unPassClient/', unPassClient),
    path('applyClient/', applyClient),
    path('searchClients/', searchClients),
    path('getClients/', getClients),
    # Worker***************************************************
    # 管理工人
    path('addWorker/', addWorker),
    path('showWorkers/', showWorkers),
    path('modifyWorker/', modifyWorker),
    path('deleteWorker/', deleteWorker),
    path('submitWorker/', submitWorker),
    path('passWorker/', passWorker),
    path('unPassWorker/', unPassWorker),
    path('applyWorker/', applyWorker),
    path('searchWorkers/', searchWorkers),
    path('getWorkers/', getWorkers),

    # Expense***************************************************
    # 管理支出
    path('addExpense/', addExpense),
    path('showExpenses/', showExpenses),
    path('modifyExpense/', modifyExpense),
    path('deleteExpense/', deleteExpense),
    path('submitExpense/', submitExpense),
    path('passExpense/', passExpense),
    path('unPassExpense/', unPassExpense),
    path('applyExpense/', applyExpense),
    path('searchExpenses/', searchExpenses),

    # Order***************************************************
    # 管理支出
    path('addOrder/', addOrder),
    path('showOrders/', showOrders),
    path('modifyOrder/', modifyOrder),
    path('deleteOrder/', deleteOrder),
    path('submitOrder/', submitOrder),
    path('passOrder/', passOrder),
    path('unPassOrder/', unPassOrder),
    path('applyOrder/', applyOrder),
    path('searchOrders/', searchOrders),


    path('', showIndex),
]
