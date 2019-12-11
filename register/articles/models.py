from django.db import models


# Create your models here.
from register.models import LoginUser


class Articles(models.Model):
    articles_name = models.CharField(max_length=128, unique=True, verbose_name="办公用品名称")
    specs = models.CharField(max_length=255, null=True, verbose_name="办公用品规格")
    remarks = models.CharField(max_length=255, null=True, verbose_name="备注")
    c_time = models.DateTimeField('创建时间', auto_now_add=True)
    creator = models.ForeignKey(LoginUser, verbose_name='创建人', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.articles_name

    class Meta:
        verbose_name_plural = '办公用品信息'
        verbose_name = '办公用品信息'
