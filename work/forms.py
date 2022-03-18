from django import forms
from django.forms import ModelForm
from work.models import Company


class CompanyForm(ModelForm):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-input'}))
    location = forms.CharField(label='Расположение', widget=forms.TextInput(attrs={'class': 'form-input'}))
    employee_count = forms.IntegerField(label='Количество работников', min_value=1)
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-input'}))
    logo = forms.ImageField(label='Логотип')


    class Meta:
        model = Company
        fields = ('name', 'logo', 'location', 'employee_count', 'description',)