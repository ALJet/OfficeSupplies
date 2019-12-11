from django.urls import path
from .views import index_stock

urlpatterns = [
    path('index/', index_stock, name='index_stock')
]
