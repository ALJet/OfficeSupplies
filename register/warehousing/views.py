import xlrd
from django.db import transaction

from register.tool import login, logout, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Warehousing
from register.warehousing import forms
from register.articles.models import Articles
from register.views import import_excel
from time import strftime
import time
from register.views import get_user


# Create your views here.


@login_required
def index_warehousing(request):
    warehousings = Warehousing.objects.all()
    return render(request, 'warehousing/index_warehousing.html', locals())


@login_required
def total_warehousing(request):
    warehousings = Warehousing.objects.all()
    warehousings = list(warehousings)
    tmp_warehousing = warehousings
    for p in warehousings:
        for m in tmp_warehousing:
            if p.article_id == m.article_id and p.id != m.id:
                p.warehousing_num = p.warehousing_num + m.warehousing_num
                warehousings.remove(m)

    to_day = strftime("%Y-%m-%d", time.localtime())
    return render(request, 'warehousing/total_warehousing.html', locals())


def add_warehousing(request):
    warehousing_form = forms.WareHousingForm(request.POST)
    if request.method == 'POST':
        message = '请检查填写内容'
        if warehousing_form.is_valid():
            articles_name = warehousing_form.cleaned_data['articles_name']
            warehousing_num = warehousing_form.cleaned_data['warehousing_num']
            remarks = warehousing_form.cleaned_data['remarks']
            warehousing_date = warehousing_form.cleaned_data['warehousing_date']

            new_warehousing = Warehousing()
            articles = Articles.objects.filter(articles_name=articles_name).first()
            new_warehousing.article = articles
            new_warehousing.warehousing_date = warehousing_date
            new_warehousing.remarks = remarks
            new_warehousing.warehousing_num = warehousing_num
            new_warehousing.creator = get_user(request.session['user_name'])
            new_warehousing.save()
            message = '添加成功!'
            return HttpResponseRedirect(reverse('register:index_warehousing'))
    return render(request, 'warehousing/add_warehousing.html', locals())


@login_required
def edit_warehousing(request, warehousing_id):
    warehousing_form = forms.WareHousingForm(request.POST)
    if request.method == 'POST':
        message = '请检查填写内容'
        if warehousing_form.is_valid():
            articles_name = warehousing_form.cleaned_data['articles_name']
            warehousing_num = warehousing_form.cleaned_data['warehousing_num']
            remarks = warehousing_form.cleaned_data['remarks']
            warehousing_date = warehousing_form.cleaned_data['warehousing_date']

            warehousing = Warehousing.objects.get(id=warehousing_id)
            articles = Articles.objects.filter(articles_name=articles_name).first()
            warehousing.article = articles
            warehousing.warehousing_num = warehousing_num
            warehousing.warehousing_date = warehousing_date
            warehousing.remarks = remarks
            # warehousing.creator = get_user(request.session['user'])
            warehousing.save()
            message = '修改成功!'
            return HttpResponseRedirect(reverse('register:index_warehousing'))
        else:
            message = '修改失败'
            warehousing_form = forms.WareHousingForm()
            return render(request, 'warehousing/edit_warehousing.html', {'purchasing_form': warehousing_form})
    else:
        articles = Warehousing.objects.only('article').get(id=warehousing_id).article
        warehousing_num = Warehousing.objects.only('warehousing_num').get(id
                                                                          =warehousing_id).warehousing_num
        warehousing_date = Warehousing.objects.only('warehousing_date').get(
            id=warehousing_id).warehousing_update_date
        remarks = Warehousing.objects.only('remarks').get(id
                                                          =warehousing_id).remarks
        warehousing_date = warehousing_date.strftime('%Y-%m-%d %H:%M:%S')
        form = forms.WareHousingForm(
            initial={
                'articles_name': articles,
                'warehousing_num': warehousing_num,
                'warehousing_date': warehousing_date,
                'remarks': remarks
            }
        )
    return render(request, 'warehousing/edit_warehousing.html', {'warehousing_form': form})


@login_required
def del_warehousing(request, warehousing_id):
    Warehousing.objects.get(id=warehousing_id).delete()
    return HttpResponseRedirect(reverse('register:index_warehousing'))


# @login_required
# def import_warehousing(request):
#     import_excel(request, 2)


@login_required
def import_warehousing(request):
    warehousings = Warehousing.objects.all()
    if request.method == 'POST':
        myFile = request.FILES.get('my_file', None)
        if not myFile:
            message = '没有选择文件，请重新选择！'
            return render(request, 'warehousing/index_warehousing.html', locals())

        else:
            type_excel = myFile.name.split('.')[1]
            if 'xlsx' == type_excel or 'xls' == type_excel:
                wb = xlrd.open_workbook(filename=None, file_contents=myFile.read())
                table = wb.sheets()[0]
                nrows = table.nrows  # 行数
                ncole = table.ncols  # 列数
                if nrows == 0:
                    message = '数据不能为空！'
                    return render(request, 'warehousing/index_warehousing.html', locals())
                try:
                    with transaction.atomic():
                        for i in range(1, nrows):
                            rowValues = table.row_values(i)
                            # product_name = rowValues[1]
                            print('rowValues', rowValues)
                            if rowValues[1] and rowValues[1] != '':

                                articles = Articles.objects.filter(articles_name=rowValues[1]).first()
                                if articles:
                                    # 转换日期格式 django读取excel会把日期变成浮点型需要进行转换
                                    date = xlrd.xldate.xldate_as_datetime(rowValues[3], 0)
                                    print('date:', date)
                                    Warehousing.objects.create(article=articles, warehousing_num=int(rowValues[2]),

                                                               creator=get_user(request.session['user_name']),
                                                               remarks=rowValues[4])
                                    # Warehousing.objects.create(article=articles, warehousing_num=int(rowValues[2]),
                                    #
                                    #                            creator=get_user(request.session['user_name']),
                                    #                            remarks=rowValues[4])

                except Exception:
                    message = '格式有误！或数据有重复！请检查后重试！'
                message = '导入成功！'
                warehousings = Warehousing.objects.all()
                return render(request, 'warehousing/index_warehousing.html', locals())
    message = '请选择Excel文件,后重试！'
    return render(request, 'warehousing/index_warehousing.html', locals())
