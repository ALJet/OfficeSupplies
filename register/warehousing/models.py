from django.db import models

# Create your models here.
from register.articles.models import Articles
from register.models import LoginUser
from django.utils import timezone


class Warehousing(models.Model):
    article = models.ForeignKey(Articles, null=False, verbose_name='用品名称', on_delete=models.CASCADE)
    warehousing_num = models.IntegerField(null=False, default=1, verbose_name='入库数量')
    warehousing_date = models.DateTimeField(verbose_name='入库时间', null=False, default=timezone.now)
    warehousing_update_date = models.DateTimeField('修改时间', null=False, auto_now=True)
    creator = models.ForeignKey(LoginUser, verbose_name='创建人', blank=True, null=True, on_delete=models.SET_NULL)
    remarks = models.CharField(max_length=255, null=True, verbose_name="入库备注")

    class Meta:
        verbose_name = '入库单'
        verbose_name_plural = '入库单'
        ordering = ['-warehousing_date']
