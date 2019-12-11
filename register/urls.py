from django.urls import path, include
from register.articles import urls as articles_url
from register.exwarehouse import urls as exwarehouse_url
from register.stock import urls as stock_urs
from register.warehousing import urls as warehousing_url
from .views import login_view, logout_view

app_name = 'register'
urlpatterns = [
    path('', login_view),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('articles/', include(articles_url)),
    path('exwarehouse/', include(exwarehouse_url)),
    path('stock/', include(stock_urs)),
    path('warehousing/', include(warehousing_url)),

]
