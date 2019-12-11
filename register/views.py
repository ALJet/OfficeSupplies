import xlrd

from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import LoginUser
from register.articles.models import Articles
from register.warehousing.models import Warehousing
from register.exwarehouse.models import ExWarehouse
from register.models import Department, User
from .tool import login, logout, login_required


# Create your views here.

# User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        message = "所有字段都必须填写！"
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()

            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = LoginUser.objects.filter(username=username).first()
                if user:
                    query = Q(username=username) & Q(password=password)
                    user = LoginUser.objects.filter(query).first()

                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            # request.session['user'] = user
                            request.session['user_name'] = user.username
                            leader = is_leader(request)
                            if leader:
                                return HttpResponseRedirect(reverse('register:index_stock'))
                            else:
                                return HttpResponseRedirect(reverse('register:index_ex_warehouse', kwargs={'case': 1}))
                    else:
                        message = "密码不正确！"

                else:
                    message = "用户不存在！"
            except:
                message = "用户不存在！"

        return render(request, 'login.html', {"message": message})
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("register:login"))


@login_required
def is_leader(request):
    leader = LoginUser.objects.filter(username=request.session['user_name']).values('is_leader')
    return leader[0]['is_leader']


@login_required
def import_excel(request, case):
    if request.method == 'POST':
        myFile = request.FILES.get('my_file', None)
        if not myFile:
            message = '没有选择文件，请重新选择！'
            re_not_file(request, case)

        else:
            type_excel = myFile.name.split('.')[1]
            if 'xlsx' == type_excel or 'xls' == type_excel:
                wb = xlrd.open_workbook(filename=None, file_contents=myFile.read())
                table = wb.sheets()[0]
                nrows = table.nrows  # 行数
                ncole = table.ncols  # 列数
                if nrows == 0:
                    message = '数据不能为空！'
                    re_not_file(request, case)
                try:
                    with transaction.atomic():
                        for i in range(1, nrows):
                            rowValues = table.row_values(i)
                            # product_name = rowValues[1]
                            if rowValues[1] and rowValues[1] != '':
                                if case == 1:
                                    Articles.objects.create(articles_name=rowValues[1], specs=rowValues[2],
                                                            remarks=rowValues[3],
                                                            creator=get_user(request.session['user_name']))
                                elif case == 2:
                                    articles = Articles.objects.filter(articles_name=rowValues[1])
                                    if articles:
                                        # 转换日期格式 django读取excel会把日期变成浮点型需要进行转换
                                        date = xlrd.xldate.xldate_as_datetime(rowValues[3], 0)

                                    Warehousing.objects.create(article=articles, warehousing_num=rowValues[2],
                                                               warehousing_date=date,
                                                               creator=get_user(request.session['user_name']),
                                                               remarks=rowValues[5])
                                elif case == 3:
                                    articles = Articles.objects.filter(articles_name=rowValues[1])
                                    department = Department.objects.filter(rowValues[3])
                                    requisition = LoginUser.objects.filter(rowValues[4])
                                    validator = LoginUser.objects.filter(rowValues[5])
                                    if articles and department and request and validator:
                                        # 转换日期格式 django读取excel会把日期变成浮点型需要进行转换
                                        date = xlrd.xldate.xldate_as_datetime(rowValues[6], 0)
                                        ExWarehouse.objects.create(articles=articles, ex_warehouse_num=rowValues[2],
                                                                   ex_warehouse_date=rowValues[3],
                                                                   department=rowValues[4],
                                                                   requisition=rowValues[5], validator=rowValues[6],
                                                                   remarks=rowValues[7], status_label=rowValues[8],
                                                                   status=1,
                                                                   creator=get_user(request.session['user_name']))



                except Exception:
                    message = '格式有误！或数据有重复！请检查后重试！'
                message = '导入成功！'
                re_not_file(request, case)
    message = '请选择Excel文件,后重试！'
    re_not_file(request, case)


def re_not_file(request, case):
    if case == 1:

        return render(request, 'articles/index_articles.html', locals())
    elif case == 2:
        return render(request, 'warehousing/index_warehousing.html', locals())
    elif case == 3:
        return render(request, 'exwarehouse/index_exwarehouse.html', locals())


def get_user(username):
    user = LoginUser.objects.filter(username=username).first()
    return user
