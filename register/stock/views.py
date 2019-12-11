from django.shortcuts import render

# from django.contrib.auth.decorators import login_required
from register.warehousing.models import Warehousing
from register.exwarehouse.models import ExWarehouse
from time import strftime
import time
from register.tool import login, logout, login_required

# Create your views here.


@login_required
def index_stock(request):
    warehousings = Warehousing.objects.all()
    warehousings = list(warehousings)
    for w in warehousings:
        for m in warehousings:
            if w.article_id == m.article_id and w.id != m.id:
                w.warehousing_num = w.warehousing_num + m.warehousing_num
                warehousings.remove(m)

    exwarehouses = ExWarehouse.objects.all()
    exwarehouses = list(exwarehouses)
    for e in exwarehouses:
        for m in exwarehouses:
            if e.article_id == m.article_id and e.id != m.id :
                e.ex_warehouse_num = e.ex_warehouse_num + m.ex_warehouse_num
                exwarehouses.remove(m)
    for w in warehousings:
        for e in exwarehouses:
            if w.article_id == e.article_id and e.status == 2:
                w.warehousing_num = w.warehousing_num - e.ex_warehouse_num
    to_date = strftime("%Y-%m-%d", time.localtime())
    stocks = warehousings
    return render(request, 'stock/index_stock.html', locals())

