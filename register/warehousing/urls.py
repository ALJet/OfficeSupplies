from django.urls import path
from .views import index_warehousing, total_warehousing, add_warehousing, del_warehousing, edit_warehousing, \
    import_warehousing

urlpatterns = [
    path('index/', index_warehousing, name='index_warehousing'),
    path('total/', total_warehousing, name='total_warehousing'),
    path('add/', add_warehousing, name='add_warehousing'),
    path('edit/<int:warehousing_id>/', edit_warehousing, name='edit_warehousing'),
    path('del/<int:warehousing_id>/', del_warehousing, name='del_warehousing'),
    path('import/', import_warehousing, name='import_warehousing'),

]
