from django import forms
from register.articles.models import Articles
from .models import Warehousing


class WareHousingForm(forms.Form):
    article = Articles.objects.all()
    articles_name = forms.ModelChoiceField(label='办公用品名称', queryset=article)
    warehousing_num = forms.IntegerField(label='入库数量',
                                         widget=forms.TextInput(attrs={'class': 'form-control'}))

    warehousing_date = forms.DateTimeField(label='入库时间', widget=forms.TextInput(attrs={'class': 'form-control'}))
    remarks = forms.CharField(label='入库备注', max_length=128,
                              widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    # class Meta:
    #     model = Warehousing
    #     fields = ['article', 'warehousing_num', 'warehousing_date', 'remarks']
