# from django.contrib.auth.decorators import login_required
# from register.tool import login_required
import xlrd
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import ExWarehouse
from register.exwarehouse import forms
from register.articles.models import Articles
from register.views import import_excel
from time import strftime
import time
from register.models import Department, LoginUser
from register.views import is_leader, get_user
from register.tool import login, logout, login_required
from register.views import get_user


# Create your views here.


@login_required
def index_ex_warehouse(request, case=None):
    to_be_processed = False
    leader = is_leader(request)
    validator_name = request.session.get('user_name')
    validator = get_user(validator_name)
    if leader:
        if case == 1:
            ex_warehouses = ExWarehouse.objects.filter(status=3)
            to_be_processed = True
        else:
            ex_warehouses = ExWarehouse.objects.all()
    else:
        count = ExWarehouse.objects.filter(validator=validator).count()
        if count == 0:
            ex_warehouses = None
        else:
            if case == 1:
                ex_warehouses = ExWarehouse.objects.filter(validator=validator).filter(status=1)
            elif case == 2:
                ex_warehouses = ExWarehouse.objects.filter(validator=validator).filter(status=2)
            else:
                ex_warehouses = ExWarehouse.objects.filter(validator=validator).all()
    return render(request, 'exwarehouse/index_exwarehouse.html', locals())


@login_required
def total_ex_warehouse(request):
    ex_warehouses = ExWarehouse.objects.all()
    ex_warehouses = list(ex_warehouses)
    tmp_ex_warehouses = ex_warehouses
    for p in ex_warehouses:
        for m in tmp_ex_warehouses:
            if p.article_id == m.article_id and p.id != m.id:
                p.ex_warehouse_num = p.ex_warehouse_num + m.ex_warehouse_num
                ex_warehouses.remove(m)

    to_day = strftime("%Y-%m-%d", time.localtime())
    return render(request, 'exwarehouse/total_exwarehouse.html', locals())


@login_required
def add_ex_warehouse(request):
    ex_warehouse_form = forms.ExWareHouseForm(request.POST)
    if request.method == 'POST':
        message = '请检查填写内容'
        if ex_warehouse_form.is_valid():
            articles_name = ex_warehouse_form.cleaned_data['articles_name']
            ex_warehouse_num = ex_warehouse_form.cleaned_data['ex_warehouse_num']
            department_name = ex_warehouse_form.cleaned_data['department']
            requisition_name = ex_warehouse_form.cleaned_data['requisition']
            validator_name = ex_warehouse_form.cleaned_data['validator']
            ex_warehouse_date = ex_warehouse_form.cleaned_data['ex_warehouse_date']
            remarks = ex_warehouse_form.cleaned_data['remarks']
            status_label = ex_warehouse_form.cleaned_data['status_label']

            new_ex_warehouse = ExWarehouse()
            articles = Articles.objects.filter(articles_name=articles_name).first()
            department = Department.objects.filter(name=department_name).first()
            validator = LoginUser.objects.filter(username=validator_name).first()
            # requisition = LoginUser.objects.filter(username=requisition_name).filter(department=department).first()
            new_ex_warehouse.article = articles
            new_ex_warehouse.ex_warehouse_date = ex_warehouse_date
            new_ex_warehouse.remarks = remarks
            new_ex_warehouse.ex_warehouse_num = ex_warehouse_num
            new_ex_warehouse.department = department
            new_ex_warehouse.requisition = requisition_name
            new_ex_warehouse.validator = validator
            new_ex_warehouse.status_label = status_label
            new_ex_warehouse.creator = get_user(request.session['user_name'])
            # 生成新的出库单状态为1
            new_ex_warehouse.status = 1
            new_ex_warehouse.save()
            message = '添加成功!'
            return HttpResponseRedirect(reverse('register:index_ex_warehouse'))
    return render(request, 'exwarehouse/add_exwarehouse.html', locals())


@login_required
def edit_ex_warehouse(request, ex_warehouse_id):
    ex_warehouse_form = forms.ExWareHouseForm(request.POST)
    if request.method == 'POST':
        message = '请检查填写内容'
        if ex_warehouse_form.is_valid():
            articles_name = ex_warehouse_form.cleaned_data['articles_name']
            ex_warehouse_num = ex_warehouse_form.cleaned_data['ex_warehouse_num']
            department_name = ex_warehouse_form.cleaned_data['department']
            requisition_name = ex_warehouse_form.cleaned_data['requisition']
            validator_name = ex_warehouse_form.cleaned_data['validator']
            ex_warehouse_date = ex_warehouse_form.cleaned_data['ex_warehouse_date']
            remarks = ex_warehouse_form.cleaned_data['remarks']
            status_label = ex_warehouse_form.cleaned_data['status_label']

            ex_warehouse = ExWarehouse.objects.get(id=ex_warehouse_id)
            articles = Articles.objects.filter(articles_name=articles_name).first()
            department = Department.objects.filter(name=department_name).first()
            validator = LoginUser.objects.filter(username=validator_name).first()
            # requisition = LoginUser.objects.filter(username=requisition_name).first()
            ex_warehouse.article = articles
            ex_warehouse.ex_warehouse_date = ex_warehouse_date
            ex_warehouse.remarks = remarks
            ex_warehouse.ex_warehouse_num = ex_warehouse_num
            ex_warehouse.department = department
            ex_warehouse.requisition = requisition_name
            ex_warehouse.validator = validator
            ex_warehouse.status_label = status_label
            ex_warehouse.status = 1
            # warehousing.creator = request.session['user']
            ex_warehouse.save()
            message = '修改成功!'
            return HttpResponseRedirect(reverse('register:index_ex_warehouse'))
        else:
            message = '修改失败'
            ex_warehouse_form = forms.ExWareHouseForm()
            return render(request, 'exwarehouse/edit_exwarehouse.html', {'ex_warehouse_form': ex_warehouse_form})
    else:
        articles = ExWarehouse.objects.only('article').get(id=ex_warehouse_id).article
        ex_warehouse_num = ExWarehouse.objects.only('ex_warehouse_num').get(id
                                                                            =ex_warehouse_id).ex_warehouse_num
        ex_warehouse_date = ExWarehouse.objects.only('ex_warehouse_date').get(
            id=ex_warehouse_id).ex_warehouse_date
        remarks = ExWarehouse.objects.only('remarks').get(id
                                                          =ex_warehouse_id).remarks
        ex_warehouse_date = ex_warehouse_date.strftime('%Y-%m-%d %H:%M:%S')
        department = ExWarehouse.objects.only('department').get(id=ex_warehouse_id).department
        requisition = ExWarehouse.objects.only('requisition').get(id=ex_warehouse_id).requisition
        validator = ExWarehouse.objects.only('validator').get(id=ex_warehouse_id).validator
        status_label = ExWarehouse.objects.only('status_label').get(id=ex_warehouse_id).status_label
        form = forms.ExWareHouseForm(
            initial={
                'articles_name': articles,
                'ex_warehouse_num': ex_warehouse_num,
                'ex_warehouse_date': ex_warehouse_date,
                'remarks': remarks,
                'department': department,
                'requisition': requisition,
                'validator': validator,
                'status_label': status_label,

            }
        )
    return render(request, 'exwarehouse/edit_exwarehouse.html', {'ex_warehouse_form': form})


'''确认出库'''


@login_required
def confirm_ex_warehouse(request, ex_warehouse_id):
    ex_warehouse = ExWarehouse.objects.get(id=ex_warehouse_id)
    ex_warehouse.status = 2
    ex_warehouse.save()
    return HttpResponseRedirect(reverse('register:index_ex_warehouse', kwargs={'case': 2}))


@login_required
def reject_ex_warehouse(request, ex_warehouse_id):
    ex_warehouse = ExWarehouse.objects.get(id=ex_warehouse_id)
    ex_warehouse.status = 3
    ex_warehouse.save()
    return HttpResponseRedirect(reverse('register:index_ex_warehouse', kwargs={'case': 1}))


@login_required
def del_ex_warehouse(request, ex_warehouse_id):
    ExWarehouse.objects.get(id=ex_warehouse_id).delete()
    return HttpResponseRedirect(reverse('register:index_ex_warehouse'))


# @login_required
# def import_ex_warehouse(request):
#     import_excel(request, 3)

@login_required
def import_ex_warehouse(request):
    ex_warehouses = ExWarehouse.objects.all()
    if request.method == 'POST':
        myFile = request.FILES.get('my_file', None)
        if not myFile:
            message = '没有选择文件，请重新选择！'
            return render(request, 'exwarehouse/index_exwarehouse.html', locals())

        else:
            type_excel = myFile.name.split('.')[1]
            if 'xlsx' == type_excel or 'xls' == type_excel:
                wb = xlrd.open_workbook(filename=None, file_contents=myFile.read())
                table = wb.sheets()[0]
                nrows = table.nrows  # 行数
                ncole = table.ncols  # 列数
                if nrows == 0:
                    message = '数据不能为空！'
                    return render(request, 'exwarehouse/index_exwarehouse.html', locals())
                try:
                    with transaction.atomic():
                        for i in range(1, nrows):
                            rowValues = table.row_values(i)
                            # product_name = rowValues[1]
                            if rowValues[1] and rowValues[1] != '':

                                articles = Articles.objects.filter(articles_name=rowValues[1]).first()
                                department = Department.objects.filter(rowValues[3])
                                requisition = LoginUser.objects.filter(rowValues[4])
                                validator = LoginUser.objects.filter(rowValues[5])
                                if articles and department and request and validator:
                                    # 转换日期格式 django读取excel会把日期变成浮点型需要进行转换
                                    date = xlrd.xldate.xldate_as_datetime(rowValues[6], 0)
                                    ExWarehouse.objects.create(articles=articles, ex_warehouse_num=int(rowValues[2]),
                                                               ex_warehouse_date=rowValues[3],
                                                               department=rowValues[4],
                                                               requisition=rowValues[5], validator=rowValues[6],
                                                               remarks=rowValues[7], status_label=rowValues[8],
                                                               status=1,
                                                               creator=get_user(request.session['user_name']))
                except Exception:
                    message = '格式有误！或数据有重复！请检查后重试！'
                message = '导入成功！'
                ex_warehouses = ExWarehouse.objects.all()
                return render(request, 'exwarehouse/index_exwarehouse.html', locals())
    message = '请选择Excel文件,后重试！'
    return render(request, 'exwarehouse/index_exwarehouse.html', locals())
