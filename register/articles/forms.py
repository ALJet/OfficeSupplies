from django import forms
from .models import Articles


class ArticleForm(forms.Form):
    articles_name = forms.CharField(label='办公用品名称', max_length=128,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    specs = forms.CharField(label='办公用品规格', max_length=128,
                            widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    remarks = forms.CharField(label='备注', max_length=128,
                              widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    # class Meta:
    #     model = Articles
    #     fields = ['articles_name', 'specs', 'remarks']
