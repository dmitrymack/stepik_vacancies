from django import forms
from django.forms import ModelForm
from work.models import Company, Vacancy, Specialty, Application, Resume


class CompanyForm(ModelForm):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-input'}))
    location = forms.CharField(label='Расположение', widget=forms.TextInput(attrs={'class': 'form-input'}))
    employee_count = forms.IntegerField(label='Количество работников', min_value=1)
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-input'}))
    logo = forms.ImageField(label='Логотип')

    class Meta:
        model = Company
        fields = ('name', 'logo', 'location', 'employee_count', 'description')


class VacancyForm(ModelForm):
    title = forms.CharField(label='Название вакансии', widget=forms.TextInput(attrs={'class': 'form-input'}))
    speciality = forms.ModelChoiceField(label='Специальность', queryset=Specialty.objects.all(), empty_label=None)
    salary_min = forms.IntegerField(label='Зарплата от', min_value=1)
    salary_max = forms.IntegerField(label='Зарплата до', min_value=1)
    skills = forms.CharField(label='Требуемые навыки', widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}))
    description = forms.CharField(label='Описание вакансии', widget=forms.Textarea(attrs={'class': 'form-input'}))

    class Meta:
        model = Vacancy
        fields = ('title', 'speciality', 'salary_min', 'salary_max', 'skills', 'description')


class ApplicationForm(ModelForm):
    written_username = forms.CharField(label='Ваше ФИО', widget=forms.TextInput(attrs={'class': 'form-input'}))
    written_phone = forms.IntegerField(label='Ваш телефон')
    written_cover_letter = forms.CharField(label='Сопроводительное письмо',
                                           widget=forms.Textarea(attrs={'class': 'form-input'}),
                                           )

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')


class ResumeForm(ModelForm):
    name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    surname = forms.CharField(label='Ваша фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    status = forms.ChoiceField(label='Готовность к работе', choices=[
        ('0', "Не ищу работу"),
        ('1', "Рассматриваю предложения"),
        ('2', "Ищу работу"),
    ])
    salary = forms.IntegerField(label='Желаемое вознаграждение')
    specialty = forms.ModelChoiceField(label='Специальность', queryset=Specialty.objects.all(), empty_label=None)
    grade = forms.ChoiceField(label='Квалификация', choices=(
        ('0', "Стажер"),
        ('1', "Джуниор"),
        ('2', "Миддл"),
        ('3', "Синьор"),
        ('4', "Лид"),
    ))
    education = forms.CharField(label='Образование', widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}))
    experience = forms.CharField(label='Опыт работы', widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 5}))
    portfolio = forms.URLField(label='Ссылка на портфолио')

    class Meta:
        model = Resume
        fields = ('name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio')
