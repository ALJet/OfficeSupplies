from django import forms


class StockForm(forms.Form):
    article_name = forms.CharField(label='办公用品名称', max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    stock_num = forms.IntegerField(label='库存数量',
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    stock_date = forms.DateTimeField(label='时间', widget=forms.TextInput(attrs={'class': 'form-control'}))
