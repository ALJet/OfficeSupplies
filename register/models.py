from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Department(models.Model):
    name = models.CharField('名称', max_length=50, help_text='部门名称')
    parent_dept_id = models.ForeignKey('self', verbose_name='上级部门id', null=True, blank=True, default=0,
                                       on_delete=models.SET_NULL)
    label = models.CharField('标签', max_length=50, blank=True, null=True, default='')
    remarks = models.CharField(max_length=155, null=True, blank=True, verbose_name="备注")
    c_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "部门"
        verbose_name_plural = "部门"


# class LoginUser(User):
#     gender = (
#         ('male', "男"),
#         ('female', "女"),
#     )
#
#     sex = models.CharField('性别', max_length=32, choices=gender, default="男")
#     is_leader = models.BooleanField('领导', default=False)
#     department = models.ForeignKey(Department, verbose_name='部门',blank=True, null=True, on_delete=models.SET_NULL)
#     c_time = models.DateTimeField('创建时间', auto_now_add=True)
#     creator = models.ForeignKey('self', verbose_name='创建人', blank=True, null=True, on_delete=models.SET_NULL)
#
#     def __str__(self):
#         return self.username
#
#     class Meta:
#         ordering = ["-c_time"]
#         verbose_name = "登录用户"
#         verbose_name_plural = "登录用户"

class LoginUser(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    username = models.CharField('用户名', max_length=128, unique=True)
    password = models.CharField('密码', max_length=256)
    email = models.EmailField('邮箱地址', null=True)
    sex = models.CharField('性别', max_length=32, choices=gender, default="男")
    is_leader = models.BooleanField('领导', default=False)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField('已激活', default=True)
    is_admin = models.BooleanField('超级管理员', default=False)
    is_deleted = models.BooleanField('已删除', default=False)
    c_time = models.DateTimeField('创建时间', auto_now_add=True)
    creator = models.ForeignKey('self', verbose_name='创建人', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "登录用户"
        verbose_name_plural = "登录用户"
