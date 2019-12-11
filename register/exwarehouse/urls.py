from django.urls import path
from .views import index_ex_warehouse, add_ex_warehouse, total_ex_warehouse, edit_ex_warehouse, confirm_ex_warehouse, \
    del_ex_warehouse, import_ex_warehouse, reject_ex_warehouse

urlpatterns = [
    path('index/', index_ex_warehouse, name='index_ex_warehouse'),
    path('index/<int:case>', index_ex_warehouse, name='index_ex_warehouse'),
    path('total/', total_ex_warehouse, name='total_ex_warehouse'),
    path('add/', add_ex_warehouse, name='add_ex_warehouse'),
    path('edit/<int:ex_warehouse_id>/', edit_ex_warehouse, name='edit_ex_warehouse'),
    path('del/<int:ex_warehouse_id>/', del_ex_warehouse, name='del_ex_warehouse'),
    path('import/', import_ex_warehouse, name='import_ex_warehouse'),
    path('reject/<int:ex_warehouse_id>/', reject_ex_warehouse, name='reject_ex_warehouse'),
    path('confirm/<int:ex_warehouse_id>/', confirm_ex_warehouse, name='confirm_ex_warehouse'),
]
