import xlrd
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from register.articles import forms
from .models import Articles
from register.views import import_excel
from register.tool import login, logout, login_required
from register.views import get_user


# Create your views here.


@login_required
def index_article(request):
    articles = Articles.objects.all()
    return render(request, 'articles/index_articles.html', locals())


@login_required
def add_article(request):
    articles_form = forms.ArticleForm(request.POST)
    if request.method == 'POST':
        message = '请检查填写内容'
        if articles_form.is_valid():
            articles_name = articles_form.cleaned_data['articles_name']
            specs = articles_form.cleaned_data['specs']
            remarks = articles_form.cleaned_data['remarks']
            same_articles = Articles.objects.filter(articles_name=articles_name)
            if same_articles:
                message = '该办公用品已存在!'
                return render(request, 'articles/add_articles.html', locals())
            new_articles = Articles()
            new_articles.articles_name = articles_name
            new_articles.specs = specs
            new_articles.remarks = remarks
            new_articles.creator = get_user(request.session['user_name'])
            new_articles.save()
            message = '添加成功!'
            return HttpResponseRedirect(reverse('register:index_articles'))
    return render(request, 'articles/add_articles.html', locals())


@login_required
def edit_articles(request, articles_id):
    articles_form = forms.ArticleForm(request.POST)
    print('True')
    if request.method == 'POST':
        print('True 2')
        message = '请检查填写内容'
        if articles_form.is_valid():

            articles_name = articles_form.cleaned_data['articles_name']
            specs = articles_form.cleaned_data['specs']
            remarks = articles_form.cleaned_data['remarks']
            update = Articles.objects.get(id=articles_id)
            update.articles_name = articles_name
            update.specs = specs
            update.remarks = remarks
            # update.creator = get_user(request.session['user_name'])
            update.save()
            message = '修改成功!'
            return HttpResponseRedirect(reverse('register:index_articles'))
        else:
            message = '修改失败'
            articles_form = forms.ArticleForm()
            return render(request, 'articles/edit_articles.html', {'articles_form': articles_form})
    else:
        articles_name = Articles.objects.only('articles_name').get(id=articles_id).articles_name
        specs = Articles.objects.only('specs').get(id=articles_id).specs
        remarks = Articles.objects.only('remarks').get(id=articles_id).remarks
        form = forms.ArticleForm(initial={
            'articles_name': articles_name,
            'specs': specs,
            'remarks': remarks,
        })

    return render(request, 'articles/edit_articles.html', {'articles_form': form})


@login_required
def del_articles(request, articles_id):
    Articles.objects.get(id=articles_id).delete()
    return HttpResponseRedirect(reverse('register:index_articles'))


# @login_required
# def import_articles(request):
#     import_excel(request, case=1)

@login_required
def import_articles(request):
    articles = Articles.objects.all()
    if request.method == 'POST':
        myFile = request.FILES.get('my_file', None)
        if not myFile:
            message = '没有选择文件，请重新选择！'
            return render(request, 'articles/index_articles.html', locals())

        else:
            type_excel = myFile.name.split('.')[1]
            if 'xlsx' == type_excel or 'xls' == type_excel:
                wb = xlrd.open_workbook(filename=None, file_contents=myFile.read())
                table = wb.sheets()[0]
                nrows = table.nrows  # 行数
                ncole = table.ncols  # 列数
                if nrows == 0:
                    message = '数据不能为空！'
                    return render(request, 'articles/index_articles.html', locals())
                try:
                    with transaction.atomic():
                        for i in range(1, nrows):
                            rowValues = table.row_values(i)
                            # product_name = rowValues[1]
                            if rowValues[1] and rowValues[1] != '':
                                Articles.objects.create(articles_name=rowValues[1], specs=rowValues[2],
                                                        remarks=rowValues[3],
                                                        creator=get_user(request.session['user_name']))
                except Exception:
                    message = '格式有误！或数据有重复！请检查后重试！'
                message = '导入成功！'
                articles = Articles.objects.all()
                return render(request, 'articles/index_articles.html', locals())
    message = '请选择Excel文件,后重试！'
    return render(request, 'articles/index_articles.html', locals())
