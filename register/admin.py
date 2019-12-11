from django.contrib import admin
from .models import LoginUser, Department


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = [ 'username', 'password', 'sex', 'is_leader', 'department',
                    'creator', 'c_time']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_dept_id', 'label', 'remarks']


#
admin.site.register(LoginUser, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
