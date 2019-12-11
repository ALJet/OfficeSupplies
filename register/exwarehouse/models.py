from django.db import models
from register.articles.models import Articles
from django.utils import timezone
from register.models import LoginUser, Department


# Create your models here.


class ExWarehouse(models.Model):
    STATUS_STR = [
        (1, '生成出库'),
        (2, '确认出库'),
        (3, '驳回出库'),
        # (4, '确认出库'),
    ]

    article = models.ForeignKey(Articles, verbose_name='用品名称', null=False, blank=False, on_delete=models.CASCADE)
    ex_warehouse_num = models.IntegerField(null=False, default=1, verbose_name='出库数量')
    ex_warehouse_date = models.DateTimeField(verbose_name='出库时间', null=False, default=timezone.now)
    ex_warehouse_update_date = models.DateTimeField('修改时间', null=False, auto_now=True)
    creator = models.ForeignKey(LoginUser, verbose_name='创建人', related_name='creator_user', blank=True, null=True,
                                on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    # requisition = models.ForeignKey(LoginUser, verbose_name='领用人', related_name='requisition_user', blank=True, null=True,
    #                                 on_delete=models.SET_NULL)
    requisition = models.CharField(verbose_name='领用人', max_length=128, default=None
                                   )
    validator = models.ForeignKey(LoginUser, verbose_name='确认人', related_name='validator_user', blank=True, null=True,
                                  on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='出库状态', choices=STATUS_STR, default=1)
    status_label = models.CharField(max_length=255, null=True, verbose_name="说明(状态补充说明)")
    remarks = models.CharField(max_length=255, null=True, verbose_name="备注")

    class Meta:
        verbose_name = '出库单'
        verbose_name_plural = '出库单'
        ordering = ['-ex_warehouse_date']
