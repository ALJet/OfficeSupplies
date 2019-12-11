from django import forms
from register.articles.models import Articles
from register.models import LoginUser, Department
from .models import ExWarehouse


class ExWareHouseForm(forms.Form):
    article = Articles.objects.all()
    users = LoginUser.objects.all()
    articles_name = forms.ModelChoiceField(label='办公用品名称', queryset=article, )
    ex_warehouse_num = forms.IntegerField(label='出库数量',
                                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    dep = Department.objects.all()
    department = forms.ModelChoiceField(label='领用人部门', queryset=dep)
    # 暂时不想使用二级联动来选择 部门和用户 因为需要添加太多新用户(或者说我不会做forms的二级联动)
    # requisition = forms.MultipleChoiceField(queryset=Department.objects.none())
    # requisition = forms.ModelChoiceField(label='领用人',queryset=LoginUser.objects.all())
    requisition = forms.CharField(label='领用人', max_length=128,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    validator_user = LoginUser.objects.filter(is_leader=False)
    validator = forms.ModelChoiceField(label='出库人', queryset=validator_user)
    ex_warehouse_date = forms.DateTimeField(label='出库时间', widget=forms.TextInput(attrs={'class': 'form-control'}))
    remarks = forms.CharField(label='出库备注', max_length=128,
                              widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    status_label = forms.CharField(label='说明(状态补充说明)', max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)


class ExWareHouseFormConfirm(forms.Form):
    article = Articles.objects.all()
    users = LoginUser.objects.all()
    ex_id = forms.IntegerField(label='序号',disabled=True)
    article_name = forms.ModelChoiceField(label='办公用品名称', queryset=article, disabled=True)
    ex_warehouse_num = forms.IntegerField(label='出库数量',
                                          widget=forms.TextInput(attrs={'class': 'form-control'}), disabled=True)
    dep = Department.objects.all()
    department = forms.ModelChoiceField(label='领用人部门', queryset=dep, disabled=True)
    # 暂时不想使用二级联动来选择 部门和用户 因为需要添加太多新用户(或者说我不会做forms的二级联动)
    # requisition = forms.MultipleChoiceField(queryset=Department.objects.none())
    requisition = forms.CharField(label='领用人', max_length=128,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  disabled=True)
    validator = forms.ModelChoiceField(label='出库人', queryset=LoginUser.objects.all(), disabled=True)
    ex_warehouse_date = forms.DateTimeField(label='出库时间', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                            disabled=True)
    remarks = forms.CharField(label='出库备注', max_length=128,
                              widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, disabled=True)
    status_label = forms.CharField(label='说明(状态补充说明)', max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
