from django.urls import path
from .views import index_article, add_article, edit_articles, del_articles, import_articles

urlpatterns = [
    path('index/', index_article, name='index_articles'),
    path('add/', add_article, name='add_articles'),
    path('edit/<int:articles_id>/', edit_articles, name='edit_articles'),
    path('del/<int:articles_id>/', del_articles, name='del_articles'),
    path('import/', import_articles, name='import_articles'),
]
